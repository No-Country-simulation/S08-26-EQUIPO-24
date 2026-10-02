# Decisiones del Proyecto

Registro de decisiones arquitectónicas y de producto.

---

## DEC-001
**Priorizar MVP sobre plataforma completa.**

- **Fecha:** 2026-09-08
- **Contexto:** 4 semanas, equipo junior, 1 Software Engineer.
- **Decisión:** Construir MVP funcional y demostrable antes de ampliar alcance.
- **Consecuencia:** FastAPI, autenticación, base de datos y alertas quedan como futuras.

---

## DEC-002
**Streamlit como primera opción de frontend.**

- **Fecha:** 2026-09-08
- **Contexto:** Necesidad de prototipado rápido y visualización de datos.
- **Decisión:** Usar Streamlit para el dashboard MVP.
- **Consecuencia:** No se requiere frontend complejo ni API inicial.

---

## DEC-003
**FastAPI opcional.**

- **Fecha:** 2026-09-08
- **Contexto:** Solo 1 Software Engineer disponible.
- **Decisión:** No incluir FastAPI en el MVP. Es un componente futuro.
- **Consecuencia:** El dashboard consume el modelo directamente sin capa de API.

---

## DEC-004
**No seleccionar dataset antes de evaluación estructurada.**

- **Fecha:** 2026-09-08
- **Contexto:** Riesgo de elegir dataset inadecuado.
- **Decisión:** Evaluar 2-3 candidatos con la matriz de `docs/dataset_selection.md`.
- **Consecuencia:** La selección formal delayed until evaluation completes.

---

## DEC-005
**Variables derivadas permitidas, pero no datos inventados.**

- **Fecha:** 2026-09-08
- **Contexto:** Necesidad de features para el modelo.
- **Decisión:** Permitir variables derivadas con justificación técnica o de negocio. Prohibir datos históricos inventados.
- **Consecuencia:** El pipeline debe distinguir dato original, variable derivada y regla de negocio.

---

## DEC-006
**El criterio de éxito guía el backlog.**

- **Fecha:** 2026-09-08
- **Contexto:** Riesgo de scope creep.
- **Decisión:** Toda tarea se evalúa contra: identificar riesgo, comprender riesgo o priorizar.
- **Consecuencia:** Funcionalidades que no apoyan el criterio van a backlog secundario.

---

## DEC-007
**Deploy inicial en Streamlit Community Cloud.**

- **Fecha:** 2026-09-08
- **Contexto:** Necesidad de demostración rápida.
- **Decisión:** Usar Streamlit Community Cloud como primera opción.
- **Consecuencia:** Validar limitaciones de ancho de banda, privacidad y rendimiento.

---

## DEC-008
**Modelo simple antes que complejo.**

- **Fecha:** 2026-09-08
- **Contexto:** 4 semanas, datos limitados.
- **Decisión:** Baseline + modelo simple (Logistic Regression / Random Forest) antes de probar XGBoost o modelos complejos.
- **Consecuencia:** Mayor tiempo para integración y dashboard.

---

## DEC-009
**Dataset seleccionado: Microsoft Azure Predictive Maintenance.**

- **Fecha:** 2026-09-11
- **Contexto:** Evaluación comparativa de 2 candidatos (Azure PdM vs AI4I 2020) usando matriz de 20 criterios ponderados.
- **Decisión:** Seleccionar Azure PdM como dataset principal para el MVP. AI4I 2020 como validación secundaria.
- **Evidencia:** Matriz completada en `docs/dataset_selection.md`, análisis automatizado en `notebooks/01_data_exploration.ipynb` (sección 10).
- **Consecuencia:** 
  - Data Engineering: unir 5 tablas (telemetría, errores, fallas, máquinas, mantenimiento).
  - Feature Engineering: rolling windows, tendencias, RUL desde `df_maint`.
  - Modelado: time-series forecasting / classification con horizonte temporal.
  - Dashboard: riesgo por máquina con serie temporal.

---

## DEC-010
**Modelo final seleccionado: Random Forest.**

- **Fecha:** 2026-09-22
- **Contexto:** Se entrenaron y evaluaron Logistic Regression (baseline) y Random Forest sobre 4 estrategias de split temporales.
- **Decisión:** Seleccionar Random Forest (`n_estimators=100`, `max_depth=10`, `min_samples_leaf=20`, `class_weight='balanced'`, `random_state=42`) como modelo final.
- **Evidencia:** PR-AUC=0.9919, ROC-AUC=0.9999 (4 estrategias de split confirman PR-AUC > 0.99 sin data leakage). Threshold óptimo=0.5591 (precision=0.8001, recall=1.0).
- **Consecuencia:** Modelo serializado en `models/baseline_model.joblib` (2.50 MB) y servido vía `dashboard/utils/model_loader.py` con inferencia batch sobre `live_demo.parquet`.

---

## DEC-011
**Estrategia de deploy final: Streamlit Community Cloud.**

- **Fecha:** 2026-09-23
- **Contexto:** MVP funcional, modelo y datos publicados en GitHub.
- **Decisión:** Deploy inicial en Streamlit Community Cloud. El dashboard consume el modelo y datos directamente desde GitHub (rama `main`) con fallback local.
- **Consecuencia:** No se requiere infraestructura adicional para el MVP. Validar límites de ancho de banda y rendimiento en producción.

---

## DEC-012
**Arquitectura de fragmentos globales para simulación en vivo.**

- **Fecha:** 2026-09-30
- **Contexto:** Streamlit tab switching causaba errores de `@st.fragment` anidados y parpadeo (flickering) al cambiar entre pestañas Telemetría, Anomalías y Mantenimiento. El código original tenía un fragmento por pestaña para actualizaciones en vivo.
- **Decisión:** 
  1. **Bucle global único** `_global_sim_loop()` con `@st.fragment(run_every=0.8)` a nivel de módulo en `app.py` — avanza el reloj de simulación via `simulation_tick()` (actualiza `SIM_INDEX_KEY`, `SIM_TIME_KEY`, `SIM_FRAME_KEY`, `SIM_ALERT_KEY`) en **todas** las pestañas simultáneamente.
  2. **Fragmento único de telemetría** `_live_telemetry_fragment()` con `@st.fragment(run_every=0.8)` — **única fuente de verdad** para el gráfico de telemetría. Usa clave Plotly estable (`live_telemetry_main_chart`) para actualización in-place. Incluye métricas de tendencia (deltas V, vibración, presión).
  3. **Gráficos de anomalías sin fragmento** — `_render_anomaly_charts()` llamado directamente (sin decorador). FFT usa `st.empty()` + `key="fft_main_chart"` para in-place sin perder zoom/pan. Eventos filtrados por `SIM_TIME_KEY`.
- **Consecuencia:** Elimina flickering al cambiar tabs, corrige errores de fragmentos anidados, simplifica código (un solo reloj, un solo renderizador de chart), habilita actualizaciones live suaves en todas las secciones.

---

## DEC-013
**Carga dual GitHub/local con fallback para datos y modelo.**

- **Fecha:** 2026-09-23
- **Contexto:** Necesidad de carga confiable en producción que funcione offline y sea resiliente a rate limits de GitHub. El dashboard debe poder demostrarse sin conexión a internet.
- **Decisión:** 
  - **Datos** (`load_live_demo_data()` en `data_loader.py`): Intenta GitHub (`main` branch, raw URL) → fallback a local `data/processed/live_demo.parquet`. Cache con `@st.cache_data(ttl=3600)`. Sidebar `st.radio(['GitHub', 'Local'])` para forzar origen. Botón "🔄 Recargar" limpia `st.cache_data` y `st.cache_resource` y fuerza rerun.
  - **Modelo** (`get_model()` en `model_loader.py`): Intenta GitHub (`main` branch, raw URL) → fallback a local `models/baseline_model.joblib`. Cache con `@st.cache_resource(ttl=3600)`. Mismo selector de origen y botón de recarga en sidebar.
- **Consecuencia:** Dashboard 100% funcional offline, resiliente a caídas de GitHub, usuario controla fuente de datos, cache 1h reduce descargas redundantes, arquitectura consistente para datos y modelo.

---

## Próximas decisiones

- DEC-014: SHAP explainability (feature importance ya documentada, SHAP opcional).