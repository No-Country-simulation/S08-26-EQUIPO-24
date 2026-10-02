# Arquitectura

## Flujo de solución

```
DATASET (Azure PdM, 5 tablas raw)
         ↓
DATA CLEANING + JOIN → master_dataset.parquet
         ↓
FEATURE ENGINEERING → 46 features (rolling, lag, deltas, trend)
         ↓
MODEL (Random Forest) → baseline_model.joblib
         ↓
DASHBOARD LAYER (Streamlit + Simulador + Fragmentos Globales)
         ↓
DECISION (ranking, recomendación, plazos, acciones)
```

*Detalle de variables y capas en secciones siguientes.*

---

## Capas

### 1. Dataset
- Datos crudos en `data/raw/`.
- Datos procesados en `data/processed/`.

### 2. Data Cleaning
- Limpieza, tratamientos de nulos, inconsistencias, duplicados.
- Validación de calidad.
- **Variables base creadas en `master_dataset.parquet` (02_data_cleaning_EDA_integrado.ipynb):**
  - **Estáticas (df_machines, left join)**: `model` (1–4), `age` (0–20 años)
  - **Historial errores (df_errors, ventanas ≤ t via np.searchsorted)**:
    - `errors_last_24h` (int), `errors_last_7d` (int), `distinct_errors_last_24h` (int)
    - `time_since_last_error_h` (float, NaN si no hay), `has_error_recent` (0/1 flag)
  - **Historial mantenimiento (df_maint, mismas ventanas ≤ t)**:
    - `hours_since_maintenance` (float, NaN si no hay), `days_since_maintenance` (float, /24)
    - `maintenance_count_30d` (int), `time_since_last_component_replacement_h` (alias hours_since_maintenance)
    - `has_recent_maintenance` (0/1 flag, ≤ 24h)
  - **Target (df_failures, merge_asof forward)**: `failure_next_24h` (0/1, horizonte 24h, `allow_exact_matches=False`)
  - **Telemetría raw**: `datetime`, `machineID`, `volt`, `rotate`, `pressure`, `vibration`

### 3. Feature Engineering
- Variables derivadas (rolling_mean, trend, rate_of_change, etc.).
- Transformaciones para el modelo.
- **Input base**: 15 variables del master_dataset + telemetría 4 sensores → 46 features finales.

### 4. Model
- Modelo de ML entrenado en `notebooks/05_modeling.ipynb`.
- **Random Forest** con `class_weight='balanced'`, 46 features, threshold=0.5591.
- PR-AUC=0.9919, ROC-AUC=0.9999, recall=1.0, precision=0.7447.
- Ver `docs/model.md` para detalle completo.

### 5. Model Artifact
- `models/baseline_model.joblib` — 2.50 MB (entrenado con scikit-learn 1.7.2).
- Contiene: `model`, `feature_cols` (46), `decision_threshold`, métricas y metadatos temporales.
- Cargado por el dashboard para inferencia batch vía `dashboard/utils/model_loader.py`.
- Carga con estrategia GitHub → fallback local, cacheada con `@st.cache_resource(ttl=3600)`.

### 6. Streamlit
- Frontend del dashboard.
- `dashboard/app.py` — Entry point, orquestación y UI.
- `dashboard/utils/model_loader.py` — Carga del artefacto ML desde GitHub/local.
- `dashboard/utils/data_loader.py` — Carga de `live_demo.parquet` desde GitHub/local + inferencia (`compute_risk_from_model()`).
- **Nota**: `load_live_demo_data()` carga `live_demo.parquet` que ya contiene todas las variables base pre-computadas en 02_data_cleaning.
- Estrategia de origen: `st.radio('Origen de datos', ['GitHub', 'Local'])` en la sidebar.

### 7. Dashboard
- Interfaz para el responsable de mantenimiento.
- **Tab 1 — Identificar:** Ranking de riesgo (tabla + bar chart), alertas críticas.
- **Tab 2 — Comprender:** Telemetría (gráfico Plotly unificado con métricas de tendencia), histórico de errores.
- **Tab 3 — Priorizar:** Cola de intervención ordenada por `priority_score` (riesgo × criticidad), recomendación principal.
- Sidebar muestra metadatos del modelo: PR-AUC, threshold, features, fechas train/test.

### 8. Decision
- Acción de mantenimiento.

---

## Arquitectura de Fragmentos Globales (Streamlit Fragment Architecture)

El dashboard implementa una arquitectura de **fragmentos globales** para lograr actualizaciones en vivo fluidas sin parpadeo y sin errores al cambiar de pestaña:

### Bucle de simulación global — `_global_sim_loop()`
- **Ubicación**: `dashboard/app.py`, nivel de módulo (líneas ~550-558).
- **Decorador**: `@st.fragment(run_every=0.8)` — se ejecuta cada 800ms mientras la app está activa.
- **Función**: Llama a `simulation_tick(live_df, model, feature_cols, threshold)` que:
  - Avanza `SIM_INDEX_KEY` (índice en la línea temporal única de timestamps).
  - Actualiza `SIM_TIME_KEY` (timestamp actual de la reproducción).
  - Calcula `failure_probability` y `risk_level` para **todas las máquinas** en ese timestamp → `SIM_FRAME_KEY`.
  - Detecta cambios de nivel de riesgo (Crítico/Moderado) vs lectura anterior → `SIM_ALERT_KEY`.
  - Si hay cambios de riesgo, pausa la simulación y fuerza `st.rerun(scope="app")`.
- **Alcance global**: El reloj avanza en **todas** las pestañas simultáneamente (Telemetría, Anomalías, Mantenimiento).

### Fragmento de telemetría en vivo — `_live_telemetry_fragment()`
- **Ubicación**: `dashboard/app.py`, nivel de módulo (líneas ~566-580).
- **Decorador**: `@st.fragment(run_every=0.8)` — re-renderiza independientemente cada 800ms.
- **Responsabilidad**: **Única fuente de verdad** para el gráfico de telemetría (Plotly).
- **Lógica**:
  1. Lee `selected_machine` (sidebar), `demo_sim_period` (session_state).
  2. Filtra `live_df` por máquina y, si el simulador corre, por `SIM_TIME_KEY`.
  3. Toma la ventana temporal (`PERIOD_HOURS[period]`) y renombra columnas a `timestamp`, `voltage`, `vibration`, `pressure`.
  4. Llama a `render_live_telemetry_chart(chart_rows, period, is_live)` con `key="live_telemetry_main_chart"` (clave Plotly estable → actualización in-place).
  5. Renderiza 3 `st.metric` con deltas: Voltaje (V), Vibración (mm/s, `delta_color="inverse"`), Presión (bar, `delta_color="inverse"`).
- **Ventaja**: Una sola definición de fragmento, sin duplicación, sin flickering.

### Gráficos de anomalías — Renderizado directo (sin fragmento)
- **Ubicación**: `dashboard/app.py`, dentro del bloque `if st.session_state.active_section == "anomalies":` (líneas ~788-842).
- **Cambio clave**: **Eliminado** `@st.fragment(run_every=0.8)` que envolvía a `_render_anomaly_charts()`.
- **Implementación actual**: Llamada directa a `_render_anomaly_charts()` (línea 842).
- **Componentes renderizados**:
  - **Espectro FFT**: Usa `st.empty()` + `plotly_chart(key="fft_main_chart")` → actualización in-place sin perder zoom/pan del usuario.
  - **Registro crítico de eventos**: Filtrado por `SIM_TIME_KEY` (timestamp del simulador).
- **Corrección**: Resuelve errores de Streamlit por fragmentos anidados al cambiar de pestaña y elimina parpadeo (flickering).

---

## FastAPI

**Opcional. No es dependencia del MVP inicial.**

**Razón:**
- 4 semanas de proyecto.
- Equipo junior.
- 1 solo Software Engineer.
- Prioridad: producto funcional.

Se documentará como decisión de arquitectura.