"""Mini-reporte de señales: explica por qué el modelo predice falla y qué hacer."""

import html

import pandas as pd
import streamlit as st

from components.demo_simulator import FEATURE_LABELS
from utils.diagnostics import get_action_recommendation, get_root_cause

_TOP_FEATURES = 4
_SENSOR_FEATURES = ["volt", "rotate", "pressure", "vibration"]


def _label(feature: str) -> str:
    """Human-readable label for a feature."""
    return FEATURE_LABELS.get(feature, feature.replace("_", " ").title())


def _fleet_stats(live_df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Return per-feature fleet mean and std (one row, many columns)."""
    numeric = live_df[feature_cols].apply(pd.to_numeric, errors="coerce")
    return numeric.agg(["mean", "std"])


def compute_machine_signals(
    machine_id: str,
    live_df: pd.DataFrame,
    model,
    feature_cols: list[str],
    risk_row: pd.Series,
    machine_meta: pd.Series | None = None,
) -> dict:
    """Compute a signal report for a single machine.

    Args:
        machine_id:   Machine identifier (string).
        live_df:      Full live demo DataFrame (all rows, all features).
        model:        Fitted estimator with ``feature_importances_`` (or None).
        feature_cols: Ordered feature list expected by the model.
        risk_row:     Row from ``df_risk`` with risk_score, risk_level, etc.
        machine_meta: Optional row from ``df_machines`` / merged data
                       (type, location, days_since_maintenance, etc.).

    Returns:
        Dict with machine_id, risk info, sensor readings, top_signals,
        and metadata.
    """
    machine_col = "machine_id" if "machine_id" in live_df.columns else "machineID"
    mask = live_df[machine_col].astype(str) == str(machine_id)
    machine_rows = live_df[mask]

    latest = machine_rows.sort_values("datetime").iloc[-1] if not machine_rows.empty else pd.Series(dtype=float)

    fleet = _fleet_stats(live_df, feature_cols)
    fleet_mean = fleet.loc["mean"]
    fleet_std = fleet.loc["std"]

    importances = getattr(model, "feature_importances_", None)
    if importances is not None and len(importances) == len(feature_cols):
        ranked = sorted(zip(feature_cols, importances), key=lambda p: p[1], reverse=True)
    else:
        ranked = [(f, 0.0) for f in feature_cols[:10]]

    top_signals = []
    for feature, imp in ranked[:_TOP_FEATURES]:
        if feature not in latest.index:
            continue
        current_val = latest[feature]
        if pd.isna(current_val):
            continue
        try:
            current_val = float(current_val)
        except (TypeError, ValueError):
            current_val = float(current_val) if pd.notna(current_val) else 0.0

        fmean = fleet_mean.get(feature, 0.0)
        fstd = fleet_std.get(feature, 0.0)
        if fstd and fstd > 0:
            z_score = (current_val - fmean) / fstd
        else:
            z_score = 0.0

        if z_score > 0.5:
            interpretation = "↑ Elevado vs flota — contribuye al riesgo"
        elif z_score < -0.5:
            interpretation = "↓ Por debajo de la flota"
        else:
            interpretation = "Dentro del rango normal de la flota"

        top_signals.append({
            "feature": feature,
            "label": _label(feature),
            "importance": float(imp),
            "current_value": current_val,
            "fleet_avg": float(fmean) if pd.notna(fmean) else 0.0,
            "z_score": float(z_score),
            "interpretation": interpretation,
        })

    sensor_readings = {}
    for sensor in _SENSOR_FEATURES:
        if sensor in latest.index and pd.notna(latest[sensor]):
            sensor_readings[sensor] = float(latest[sensor])

    meta = {}
    if machine_meta is not None:
        meta = {
            "type": str(machine_meta.get("type", "N/D")),
            "location": str(machine_meta.get("location", "N/D")),
            "days_since_maintenance": int(machine_meta.get("days_since_maintenance", 0)),
            "operating_hours": int(machine_meta.get("operating_hours", 0)),
        }

    return {
        "machine_id": str(machine_id),
        "risk_score": float(risk_row.get("risk_score", 0)),
        "risk_level": str(risk_row.get("risk_level", "Estable")),
        "criticality": str(risk_row.get("criticality", "N/D")),
        "priority": str(risk_row.get("priority", "Ninguna")),
        "priority_score": float(risk_row.get("priority_score", 0)),
        "top_signals": top_signals,
        "sensor_readings": sensor_readings,
        "machine_meta": meta,
    }


def _risk_color(level: str) -> str:
    lc = level.lower()
    if "crit" in lc:
        return "#ff4b4b"
    if "moder" in lc:
        return "#ffa500"
    return "#28a745"


def render_mini_report(signals: dict, df_errors: pd.DataFrame, model_meta: dict | None = None) -> None:
    """Render the mini-report UI for a single machine."""
    mid = signals["machine_id"]
    risk_score = signals["risk_score"]
    risk_level = signals["risk_level"]
    color = _risk_color(risk_level)
    tone = "critical" if "crit" in risk_level.lower() else "moderate" if "moder" in risk_level.lower() else "stable"
    lamp = "critical" if tone == "critical" else "moderate" if tone == "moderate" else ""

    # ── Header ──
    st.markdown(
        f"<div class='mini-report-header' style='border-left:3px solid {color}'>"
        f"<div class='eyebrow' style='color:{color};font-weight:700'>MINI-REPORTE DE SEÑALES</div>"
        f"<h3 style='margin:.25rem 0'>{html.escape(mid)} "
        f"<span class='pill {tone}' style='font-size:.7rem'>"
        f"<i class='alert-lamp {lamp}'></i>{risk_level.upper()} · {risk_score:.1f}%</span></h3>"
        f"<div class='priority-copy'>Acción: {html.escape(signals['priority'])} "
        f"&middot; Criticidad: {html.escape(signals['criticality'])}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Sensor readings ──
    readings = signals.get("sensor_readings", {})
    if readings:
        sensor_cols = st.columns(len(readings))
        sensor_labels = {"volt": "Voltaje", "rotate": "Rotación", "pressure": "Presión", "vibration": "Vibración"}
        sensor_units = {"volt": "V", "rotate": "RPM", "pressure": "bar", "vibration": "mm/s"}
        for col, (sensor, value) in zip(sensor_cols, readings.items()):
            with col:
                st.metric(
                    sensor_labels.get(sensor, sensor),
                    f"{value:.2f} {sensor_units.get(sensor, '')}",
                )

    # ── Top signals ──
    top_signals = signals.get("top_signals", [])
    if top_signals:
        st.markdown("<div class='eyebrow' style='margin:.5rem 0 .2rem'>SEÑALES CLAVE DEL MODELO</div>", unsafe_allow_html=True)
        for sig in top_signals:
            st.markdown(
                f"<div class='sidebar-card' style='padding:.35rem .5rem;font-size:.75rem'>"
                f"<span style='color:#dae2fd;font-weight:600'>{html.escape(sig['label'])}</span>"
                f"<span style='color:#9da6bd'> · importancia: {sig['importance']*100:.1f}% "
                f"&middot; actual: {sig['current_value']:.2f} "
                f"&middot; flota: {sig['fleet_avg']:.2f}</span>"
                f"<span style='color:{color};font-family:JetBrains Mono,monospace'> · {sig['interpretation']}</span></div>",
                unsafe_allow_html=True,
            )

    # ── Root cause analysis ──
    st.markdown("<div class='eyebrow' style='margin:.5rem 0 .2rem'>ANÁLISIS DE CAUSA RAÍZ</div>", unsafe_allow_html=True)
    if df_errors is not None and not df_errors.empty:
        machine_errors = df_errors[df_errors["machine_id"].astype(str) == str(mid)].sort_values("timestamp", ascending=False).head(3)
        if machine_errors.empty:
            st.info("Sin errores registrados para este activo.")
        else:
            for _, event in machine_errors.iterrows():
                root_cause, rc_color = get_root_cause(event["error_code"])
                esc_ts = html.escape(str(event.get("timestamp", ""))[:16])
                esc_ec = html.escape(str(event.get("error_code", "")))
                esc_desc = html.escape(str(event.get("description", "")))
                st.markdown(
                    f"<div class='sidebar-card'>"
                    f"<div class='eyebrow'>{esc_ts} · "
                    f"<span style='color:{rc_color};font-weight:700'>{esc_ec}</span></div>"
                    f"<div style='color:var(--text);font-size:.72rem;margin-top:.25rem'>{esc_desc}</div>"
                    f"<div style='color:{rc_color};font-size:.65rem;margin-top:.25rem;font-family:JetBrains Mono,monospace'>{root_cause}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("Sin historial de errores disponible.")

    # ── Action recommendation ──
    action = get_action_recommendation(signals["priority"])
    st.markdown(
        f"<div class='eyebrow' style='margin:.5rem 0 .2rem'>"
        f"ACCIÓN RECOMENDADA &mdash; <span style='color:{color}'>{action['title']}</span></div>",
        unsafe_allow_html=True,
    )
    for step in action["steps"]:
        st.markdown(f"<div style='color:var(--text);font-size:.75rem;margin:.15rem 0'>• {html.escape(step)}</div>", unsafe_allow_html=True)

    # ── Model metadata ──
    if model_meta:
        st.caption(
            f"Modelo: {model_meta.get('model_type', 'RandomForest')} "
            f"&middot; PR-AUC: {model_meta.get('pr_auc', 'N/D')} "
            f"&middot; Threshold: {model_meta.get('decision_threshold', 0.5):.4f}"
        )
