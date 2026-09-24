import html

import plotly.graph_objects as go
import streamlit as st

from components.machine_detail import render_machine_detail
from components.sensor_chart import render_sensor_chart
from components.risk_table import render_risk_table
from utils.data_loader import compute_risk_from_model, load_live_demo_data
from utils.model_loader import get_model


st.set_page_config(
    page_title="Mantenimiento predictivo",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');
    :root { --bg:#0b1326; --surface:#111a2d; --surface-2:#171f33; --surface-3:#222a3d; --line:#424754; --text:#dae2fd; --muted:#9da6bd; --blue:#7eabff; --blue-strong:#4d8eff; --orange:#ffb690; --red:#ffb4ab; --green:#54e18c; }
    html, body, [class*="css"], [data-testid="stAppViewContainer"] { font-family:Inter,sans-serif; }
    [data-testid="stAppViewContainer"] { background:var(--bg); color:var(--text); }
    [data-testid="stHeader"] { background:rgba(11,19,38,.85); }
    [data-testid="stMainBlockContainer"] { max-width:none; padding:5.3rem 2rem 2.5rem; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#171f33 0%,#0b1326 100%); border-right:1px solid rgba(126,171,255,.2); }
    [data-testid="stSidebar"] > div:first-child { padding:1.25rem 1rem; }
    [data-testid="stMetric"] { background:var(--surface-2); border:1px solid rgba(126,171,255,.15); border-radius:8px; padding:1rem; }
    [data-testid="stMetricLabel"] { color:var(--muted); font-family:'JetBrains Mono',monospace; font-size:.68rem; text-transform:uppercase; letter-spacing:.06em; }
    [data-testid="stMetricValue"] { color:var(--text); font-family:'JetBrains Mono',monospace; font-weight:700; }
    [data-testid="stMetricDelta"] { font-family:'JetBrains Mono',monospace; font-size:.72rem; }
    [data-testid="stTabs"] [role="tablist"] { gap:.25rem; padding:.35rem; background:var(--surface-2); border:1px solid rgba(126,171,255,.15); border-radius:8px; }
    [data-testid="stTabs"] button[role="tab"] { color:var(--muted); border-radius:6px; font-weight:600; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:#001a42; background:var(--blue-strong); }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color:rgba(126,171,255,.14); background:rgba(23,31,51,.72); border-radius:8px; }
    [data-testid="stDataFrame"] { border:1px solid rgba(126,171,255,.14); }
    h1, h2, h3 { font-family:'Space Grotesk',sans-serif!important; letter-spacing:0!important; }
    h1 { font-size:2rem!important; color:var(--text)!important; } h2 { font-size:1.3rem!important; } h3 { font-size:1.05rem!important; }
    .mono { font-family:'JetBrains Mono',monospace; } .eyebrow { color:var(--muted); font:500 .68rem 'JetBrains Mono',monospace; letter-spacing:.1em; text-transform:uppercase; }
    .brand { color:var(--blue); font:700 1.15rem 'Space Grotesk',sans-serif; }
    .topbar { position:fixed; z-index:5; top:0; left:0; right:0; height:4rem; display:flex; align-items:center; justify-content:space-between; padding:0 2rem; background:rgba(11,19,38,.86); border-bottom:1px solid rgba(126,171,255,.15); backdrop-filter:blur(14px); }
    .status-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 8px var(--green); margin-right:.35rem; }
    .banner { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:1rem 1.2rem; background:var(--surface-2); border:1px solid rgba(126,171,255,.14); border-radius:8px; margin-bottom:1rem; }
    .banner-title { color:var(--text); font:600 1.2rem 'Space Grotesk',sans-serif; } .banner-copy { color:var(--muted); font-size:.82rem; margin-top:.25rem; }
    .pill { display:inline-block; padding:.28rem .5rem; border-radius:4px; color:var(--blue); background:rgba(77,142,255,.16); font:600 .65rem 'JetBrains Mono',monospace; letter-spacing:.04em; }
    .pill-red { color:var(--red); background:rgba(255,80,70,.16); } .pill-green { color:var(--green); background:rgba(84,225,140,.12); }
    .ai-card { padding:1rem; border:1px solid rgba(126,171,255,.3); border-radius:8px; background:linear-gradient(110deg,rgba(77,142,255,.18),rgba(23,31,51,.8)); }
    .ai-card p { color:var(--muted); font-size:.84rem; margin:.35rem 0 0; }
    .section-head { display:flex; align-items:end; justify-content:space-between; gap:1rem; margin:1.25rem 0 .8rem; } .section-head h2 { margin:0; } .section-head p { color:var(--muted); margin:.25rem 0 0; font-size:.8rem; }
    .sidebar-card { padding:.85rem; border:1px solid rgba(126,171,255,.18); border-radius:8px; background:rgba(34,42,61,.6); margin:.8rem 0; }
    .meta-row { display:flex; justify-content:space-between; gap:.5rem; padding:.25rem 0; color:var(--muted); font:.7rem 'JetBrains Mono',monospace; } .meta-row strong { color:var(--text); text-align:right; font-weight:500; }
    .priority { border-left:3px solid var(--red); padding:.9rem 1rem; background:var(--surface-2); border-radius:0 8px 8px 0; margin:.5rem 0; } .priority-title { font-weight:700; color:var(--text); } .priority-copy { color:var(--muted); font-size:.82rem; margin-top:.25rem; } .priority-meta { display:flex; flex-wrap:wrap; gap:.8rem; margin-top:.5rem; color:var(--muted); font:.68rem 'JetBrains Mono',monospace; }
    @media (max-width:800px) { [data-testid="stMainBlockContainer"] { padding:4.8rem 1rem 1.5rem; } .topbar { padding:0 1rem; } .banner { align-items:flex-start; flex-direction:column; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    st.experimental_rerun()


SECTION_OPTIONS = [
    ("overview", "1. Vista General"),
    ("telemetry", "2. Telemetria en Vivo"),
    ("anomalies", "3. Deteccion de Anomalias"),
    ("maintenance", "4. Plan de Mantenimiento"),
]


if "active_section" not in st.session_state:
    st.session_state.active_section = "overview"


def risk_figure(df_risk):
    chart = df_risk.sort_values("risk_score", ascending=True).copy()
    colors = {"Cr\u00edtico":"#ff6b68", "Moderado":"#ec6a06", "Estable":"#54e18c"}
    fig = go.Figure(go.Bar(
        x=chart["risk_score"], y=chart["machine_id"], orientation="h",
        marker_color=[colors.get(level, "#7eabff") for level in chart["risk_level"]],
        text=[f"{value:.0f}%" for value in chart["risk_score"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>Riesgo: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,14,32,.65)",
        font={"family":"JetBrains Mono", "color":"#dae2fd", "size":11},
        xaxis={"range":[0,110], "gridcolor":"rgba(140,144,159,.18)", "title":"Índice de riesgo (%)"},
        yaxis={"gridcolor":"rgba(0,0,0,0)"}, margin={"l":15,"r":45,"t":15,"b":45},
        height=max(280, len(chart) * 52), showlegend=False,
    )
    fig.add_vline(x=60, line_dash="dash", line_color="#ffb4ab", annotation_text="Umbral crítico 60%", annotation_font_color="#ffb4ab")
    return fig


def render_sidebar(df_machines, df_risk, data_source, model_source, feature_cols):
    with st.sidebar:
        st.markdown("<div class='brand'> Mantenimiento</div><div class='eyebrow'>S08-26-EQUIPO-24</div><div style='color:var(--green);font:.7rem JetBrains Mono;margin-top:.4rem'><span class='status-dot'></span>EN VIVO</div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div class='eyebrow'>NAVEGACIN OPERATIVA</div>", unsafe_allow_html=True)
        st.caption("Selecciona un modulo para cambiar de vista.")
        for section_id, label in SECTION_OPTIONS:
            if st.button(label, key=f"sidebar_{section_id}", width="stretch"):
                st.session_state.active_section = section_id
                rerun_app()
        selected_machine = st.selectbox("ID de máquina", df_machines["machine_id"].tolist())
        selected_status = st.multiselect("Filtro de estado", ["Critico", "Moderado", "Estable"], default=["Critico", "Moderado", "Estable"])
        selected_status = ["Cr\u00edtico" if status == "Critico" else status for status in selected_status]
        selected_criticality = st.multiselect("Filtro de criticidad", ["Alta", "Media", "Baja"], default=["Alta", "Media", "Baja"])
        machine_row = df_machines[df_machines["machine_id"] == selected_machine].iloc[0]
        metadata = [("ID", machine_row["machine_id"]), ("Tipo", machine_row["type"]), ("Ubicación", machine_row["location"]), ("Operación", f"{machine_row['operating_hours']} h"), ("ltimo mant.", machine_row["last_maintenance"])]
        rows = "".join(f"<div class='meta-row'><span>{label}</span><strong>{html.escape(str(value))}</strong></div>" for label, value in metadata)
        st.markdown(f"<div class='sidebar-card'><div class='eyebrow'>METADATOS · SYNC_OK</div>{rows}</div>", unsafe_allow_html=True)
        critical = int(df_risk["risk_level"].astype(str).str.startswith("Cr").sum())
        st.markdown(f"<div class='ai-card'><div style='color:var(--blue);font-weight:700'> Análisis con IA <span class='pill'>AI AGENT</span></div><p>{critical} activo(s) requieren revisión prioritaria según el modelo predictivo.</p></div>", unsafe_allow_html=True)
        st.caption(f"Datos: {data_source}")
        st.caption(f"Modelo: {model_source} · {len(feature_cols)} features")
        if st.button(" Recargar modelo y datos", width="stretch"):
            st.cache_data.clear()
            st.cache_resource.clear()
            rerun_app()
    return selected_machine, selected_status, selected_criticality


try:
    with st.spinner("Cargando datos y modelo..."):
        live_df, data_source = load_live_demo_data()
        df_machines, df_risk, df_telemetry, df_errors = compute_risk_from_model(live_df)
        model, feature_cols, meta, model_source = get_model()
except Exception as error:
    st.error(f"Error al cargar datos o modelo: {error}")
    st.stop()


selected_machine, selected_status, selected_criticality = render_sidebar(df_machines, df_risk, data_source, model_source, feature_cols)
st.markdown("<div class='topbar'><div><span class='brand'> Mantenimiento predictivo</span><div class='eyebrow'>S08-26-EQUIPO-24 · DESCUBRIMIENTO / MVP · <span style='color:var(--green)'><span class='status-dot'></span>SISTEMA ACTIVO</span></div></div><div class='mono' style='color:var(--muted);font-size:.7rem'>Streamlit Core 1.63</div></div>", unsafe_allow_html=True)
st.markdown("<div class='banner'><div><div class='banner-title'> Monitor Diagnóstico Industrial <span class='pill'>PLANTA-SUR // LÍNEA-A</span></div><div class='banner-copy'>Análisis predictivo multivariante de activos industriales en tiempo de ciclo real.</div></div><div class='pill pill-green'><span class='status-dot'></span>FRECUENCIA: 100 Hz</div></div>", unsafe_allow_html=True)

critical_count = int(df_risk["risk_level"].astype(str).str.startswith("Cr").sum())
avg_risk = float(df_risk["risk_score"].mean())
selected_risk = df_risk[df_risk["machine_id"] == selected_machine].iloc[0]
next_date = df_machines["next_maintenance"].min()
next_date_text = next_date.strftime("%d %b %Y") if not df_machines["next_maintenance"].isna().all() else "N/D"
st.markdown(f"<div class='ai-card' style='margin-bottom:1rem'><strong> Copiloto Predictivo IA  Diagnóstico de Flota</strong><span class='pill pill-green' style='margin-left:.5rem'>SÍNTESIS CONTINUA</span><p>Análisis correlacionado en {len(df_machines)} activos. <strong style='color:var(--red)'>{critical_count} activo(s)</strong> superan el umbral de criticidad operativa y requieren intervención priorizada.</p></div>", unsafe_allow_html=True)

nav_columns = st.columns(4)
for nav_column, (section_id, label) in zip(nav_columns, SECTION_OPTIONS):
    with nav_column:
        button_type = "primary" if st.session_state.active_section == section_id else "secondary"
        if st.button(label, key=f"top_{section_id}", width="stretch", type=button_type):
            st.session_state.active_section = section_id
            rerun_app()

st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)

if st.session_state.active_section == "overview":
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(" Máquinas monitoreadas", len(df_machines), f"{len(df_machines)} unidades IoT")
    with kpi2:
        st.metric("️ Riesgo crítico", critical_count, "Atención inmediata", delta_color="inverse")
    with kpi3:
        st.metric(" Próximo mantenimiento", next_date_text, "Ventana programada")
    with kpi4:
        st.metric(" Riesgo promedio", f"{avg_risk:.0f}%", "Índice global", delta_color="inverse" if avg_risk >= 60 else "normal")
    st.markdown("<div class='section-head'><div><h2>Distribución de riesgo operacional por activo</h2><p>Cálculo de probabilidad de paro técnico en las próximas 168 horas.</p></div><span class='pill'>FLEET AVG</span></div>", unsafe_allow_html=True)
    st.plotly_chart(risk_figure(df_risk), width="stretch", config={"displayModeBar": False})
    st.markdown("<div class='section-head'><div><h2>Matriz diagnóstica de flota</h2><p>Ranking calculado a partir de la última lectura disponible.</p></div></div>", unsafe_allow_html=True)
    render_risk_table(df_risk, selected_status, selected_criticality)

if st.session_state.active_section == "telemetry":
    tone = "pill-red" if str(selected_risk["risk_level"]).startswith("Cr") else "pill-green"
    st.markdown(f"<div class='section-head'><div><h2>Telemetría crítica multieje · {html.escape(selected_machine)}</h2><p>Flujo temporal y estado de señales de la máquina seleccionada.</p></div><span class='pill {tone}'>{html.escape(selected_risk['risk_level']).upper()}</span></div>", unsafe_allow_html=True)
    chart_col, detail_col = st.columns([2, 1])
    with chart_col:
        render_sensor_chart(df_telemetry, selected_machine)
    with detail_col:
        render_machine_detail(df_errors, selected_machine)
    df_selected = df_telemetry[df_telemetry["machine_id"] == selected_machine].sort_values("timestamp")
    if not df_selected.empty:
        latest, previous = df_selected.iloc[-1], df_selected.iloc[0]
        temp_col, vibration_col, pressure_col = st.columns(3)
        with temp_col:
            st.metric("Temperatura husillo", f"{latest['temperature']:.1f} °C", f"{latest['temperature'] - previous['temperature']:+.1f} °C")
        with vibration_col:
            st.metric("Vibración cojinete", f"{latest['vibration']:.2f} mm/s", f"{latest['vibration'] - previous['vibration']:+.2f} mm/s", delta_color="inverse")
        with pressure_col:
            st.metric("Presión lubricante", f"{latest['pressure']:.1f} bar", f"{latest['pressure'] - previous['pressure']:+.1f} bar")

if st.session_state.active_section == "anomalies":
    st.markdown("<div class='section-head'><div><h2>Módulo de diagnóstico y detección de anomalías</h2><p>Señales preparadas para FFT, envolvente Hilbert y clasificación multivariante.</p></div><span class='pill pill-red'>MODELO EN VIVO</span></div>", unsafe_allow_html=True)
    anomaly_col, heat_col = st.columns([1, 2])
    with anomaly_col:
        confidence = min(99.9, max(50.0, float(selected_risk["risk_score"]) + 5))
        st.markdown(f"<div class='sidebar-card'><div class='eyebrow'>ÍNDICE DE CERTEZA ALGORÍTMICA</div><div class='mono' style='font-size:1.7rem;font-weight:700;color:var(--red);margin:.55rem 0'>{confidence:.1f}%</div><div style='color:var(--muted);font-size:.74rem'>{selected_risk['risk_level']} · {selected_risk['priority']}</div></div>", unsafe_allow_html=True)
        st.progress(confidence / 100, text="Certeza del diagnóstico")
        st.caption(f"Algoritmo: {meta.get('model_type', 'modelo predictivo')} · threshold {meta.get('decision_threshold', 0.5):.3f}")
    with heat_col:
        st.markdown("<div class='section-head'><div><h3>Mapa de estado por activo</h3><p>Vista preparada para conectar subsistemas y sensores reales.</p></div></div>", unsafe_allow_html=True)
        heatmap = df_risk[["machine_id", "risk_score", "risk_level", "criticality", "priority"]].copy()
        heatmap["Riesgo"] = heatmap["risk_score"].map(lambda value: f"{value:.0f}%")
        st.dataframe(heatmap[["machine_id", "Riesgo", "risk_level", "criticality", "priority"]], hide_index=True, width="stretch")
    st.info("La visualización FFT queda reservada para conectar las ventanas de acelerómetro cuando estén disponibles en el pipeline de señales.")

if st.session_state.active_section == "maintenance":
    st.markdown("<div class='section-head'><div><h2>Plan de mantenimiento</h2><p>Cola de intervención priorizada por riesgo, criticidad e impacto operacional.</p></div><span class='pill pill-red'>ACCIN REQUERIDA</span></div>", unsafe_allow_html=True)
    ordered = df_risk.merge(df_machines[["machine_id", "type", "location", "days_since_maintenance"]], on="machine_id").sort_values("priority_score", ascending=False)
    if not ordered.empty:
        top = ordered.iloc[0]
        st.markdown(f"<div class='ai-card'><div class='eyebrow'>RECOMENDACIN PRIORITARIA #1</div><div class='banner-title'>Inspeccionar inmediatamente {html.escape(str(top['machine_id']))} · {html.escape(str(top['type']))}</div><p>Riesgo estimado <strong style='color:var(--red)'>{top['risk_score']:.0f}%</strong>. Acción sugerida: <strong>{html.escape(str(top['priority']))}</strong>. {int(top['days_since_maintenance'])} días desde el último mantenimiento.</p></div>", unsafe_allow_html=True)
    for rank, (_, row) in enumerate(ordered.iterrows(), start=1):
        tone = "var(--red)" if str(row["risk_level"]).startswith("Cr") else "var(--orange)" if row["risk_level"] == "Moderado" else "var(--green)"
        st.markdown(f"<div class='priority' style='border-left-color:{tone}'><div class='priority-title'>{rank}. {html.escape(str(row['machine_id']))}  {html.escape(str(row['type']))} <span class='pill' style='color:{tone}'>{row['risk_score']:.0f}% · {html.escape(str(row['risk_level']).upper())}</span></div><div class='priority-copy'>Ubicación: {html.escape(str(row['location']))} · Acción: {html.escape(str(row['priority']))}</div><div class='priority-meta'><span>Criticidad: {html.escape(str(row['criticality']))}</span><span>{int(row['days_since_maintenance'])} días sin mantenimiento</span><span>Prioridad: {row['priority_score']:.0f}</span></div></div>", unsafe_allow_html=True)
