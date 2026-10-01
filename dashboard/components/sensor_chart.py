"""Componente: Gráfico de telemetría de sensores (3 ejes Plotly) y espectro FFT."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def telemetry_figure(df_selected):
    """Construye el gráfico Plotly de telemetría con 3 ejes sincronizados.

    Ejes:
        y  — Voltaje (V)          línea coral sólida   #ffb4ab
        y2 — Vibración (mm/s)     línea azul sólida    #4d8eff  (derecha)
        y3 — Presión (bar)        línea celeste discontinua #a4c9ff (derecha, 96%)

    Zona sombreada: último 18% del intervalo analizado en rojo tenue.
    """
    if df_selected.empty:
        return go.Figure()

    # Normalizar nombre volt → voltage si viene del dataset crudo
    if "volt" in df_selected.columns and "voltage" not in df_selected.columns:
        df_selected = df_selected.rename(columns={"volt": "voltage"})

    figure = go.Figure()

    series = [
        ("voltage",   "Voltaje (V)",      "#ffb4ab", "solid", "y"),
        ("vibration", "Vibración (mm/s)", "#4d8eff", "solid", "y2"),
        ("pressure",  "Presión (bar)",    "#a4c9ff", "dash",  "y3"),
    ]
    for col, label, color, dash, yaxis in series:
        if col in df_selected.columns:
            figure.add_trace(go.Scatter(
                x=df_selected["timestamp"],
                y=df_selected[col],
                name=label,
                mode="lines",
                line={"color": color, "width": 2, "dash": dash},
                yaxis=yaxis,
                hovertemplate=f"<b>{label}</b>: %{{y:.2f}}<extra></extra>",
            ))

    # Zona de alerta: último 18% del eje temporal
    timestamps = df_selected["timestamp"].dropna()
    if len(timestamps) >= 2:
        t_min = timestamps.min()
        t_max = timestamps.max()
        span = (t_max - t_min).total_seconds()
        alert_start = t_min + pd.Timedelta(seconds=span * 0.82)
        figure.add_vrect(
            x0=alert_start,
            x1=t_max,
            fillcolor="rgba(147, 0, 10, 0.18)",
            opacity=1,
            line_width=0,
            annotation_text="⚠ Zona de alerta",
            annotation_font_color="#ffb4ab",
            annotation_font_size=9,
        )

    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#060e20",
        height=360,
        margin={"l": 12, "r": 72, "t": 32, "b": 35},
        hovermode="x unified",
        font={"family": "JetBrains Mono", "color": "#dae2fd", "size": 10},
        legend={"orientation": "h", "y": 1.12, "x": 0, "font": {"size": 10}},
        xaxis={
            "gridcolor": "rgba(140,144,159,.12)",
            "showgrid": True,
        },
        yaxis={
            "title": {"text": "Voltaje (V)", "font": {"color": "#ffb4ab"}},
            "gridcolor": "rgba(140,144,159,.12)",
            "tickfont": {"color": "#ffb4ab"},
        },
        yaxis2={
            "title": {"text": "Vibración (mm/s)", "font": {"color": "#4d8eff"}},
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "tickfont": {"color": "#4d8eff"},
        },
        yaxis3={
            "title": {"text": "Presión (bar)", "font": {"color": "#a4c9ff"}},
            "overlaying": "y",
            "side": "right",
            "position": 0.96,
            "showgrid": False,
            "tickfont": {"color": "#a4c9ff"},
            "anchor": "free",
        },
    )
    return figure


def fft_figure(df_selected):
    """Espectro de frecuencia FFT de la señal de vibración (0–500 Hz).

    Detecta el pico armónico más alto y lo anota con una línea discontinua.
    """
    if df_selected.empty or "vibration" not in df_selected.columns:
        return go.Figure()

    signal = df_selected["vibration"].astype(float).dropna().to_numpy()
    if len(signal) < 4:
        return go.Figure()

    signal_centered = signal - signal.mean()
    spectrum = np.abs(np.fft.rfft(signal_centered))
    # Asumir muestreo ~100 Hz (1 lectura/hora → frecuencias relativas de demostración)
    frequency = np.fft.rfftfreq(len(signal), d=1.0 / 100.0)

    figure = go.Figure(go.Scatter(
        x=frequency,
        y=spectrum,
        mode="lines",
        line={"color": "#4d8eff", "width": 2},
        fill="tozeroy",
        fillcolor="rgba(77,142,255,.12)",
        hovertemplate="Frecuencia: %{x:.1f} Hz<br>Amplitud: %{y:.2f}<extra></extra>",
    ))

    # Detectar pico dominante (excluyendo DC component en índice 0)
    if len(spectrum) > 1:
        peak_idx = int(np.argmax(spectrum[1:]) + 1)
        peak_freq = float(frequency[peak_idx])
        if peak_freq > 0:
            figure.add_vline(
                x=peak_freq,
                line_dash="dash",
                line_color="#ffb4ab",
                line_width=1.5,
                annotation_text=f"Pico {peak_freq:.0f} Hz",
                annotation_font_color="#ffb4ab",
                annotation_font_size=10,
            )

    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#060e20",
        height=270,
        margin={"l": 10, "r": 15, "t": 15, "b": 35},
        showlegend=False,
        font={"family": "JetBrains Mono", "color": "#dae2fd", "size": 10},
        xaxis={
            "title": "Frecuencia (Hz)",
            "gridcolor": "rgba(140,144,159,.12)",
            "range": [0, min(500, float(frequency.max()))],
        },
        yaxis={
            "title": "Amplitud",
            "gridcolor": "rgba(140,144,159,.12)",
        },
    )
    return figure


def render_sensor_chart(df_telemetry, machine_id):
    """Muestra el gráfico Plotly 3-ejes de telemetría para una máquina.

    Args:
        df_telemetry: DataFrame con columnas machine_id, timestamp, voltage, vibration, pressure.
        machine_id: ID de la máquina seleccionada.
    """
    if "machineID" in df_telemetry.columns:
        df_telemetry = df_telemetry.rename(columns={"machineID": "machine_id"})

    df_machine = df_telemetry[df_telemetry["machine_id"].astype(str) == str(machine_id)].copy()

    if df_machine.empty:
        st.warning(f"No hay telemetría para {machine_id}.")
        return

    df_machine = df_machine.sort_values("timestamp")

    st.plotly_chart(
        telemetry_figure(df_machine),
        width="stretch",
        config={"displayModeBar": False},
        key=f"sensor_chart_{machine_id}",
    )

    with st.expander("📋 Ver último registro"):
        latest = df_machine.iloc[-1]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Voltaje", f"{latest['voltage']:.1f} V")
        with c2:
            st.metric("Vibración", f"{latest['vibration']:.2f} mm/s")
        with c3:
            st.metric("Presión", f"{latest['pressure']:.1f} bar")
