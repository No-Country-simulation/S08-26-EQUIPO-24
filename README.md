# PredictiveMaintenance

**Código:** S08-26-EQUIPO-24

**Estado:** ✅ Completado (100%) — Modelo ML Serializado + Dashboard Streamlit con Simulador de Telemetría, Alertas Animadas e Interfaz UI/UX

**🚀 Demo en producción:** [s08-26-equipo-24git-g3stte6g7k8tr9wbnrichu.streamlit.app](https://s08-26-equipo-24git-g3stte6g7k8tr9wbnrichu.streamlit.app/)

---

## ¿Qué es?

PredictiveMaintenance es una solución de mantenimiento predictivo que permite a un responsable de mantenimiento pasar de la reactividad a la proactividad.

## Objetivo

Construir una solución que permita responder:

- ¿Qué máquinas están mostrando señales de deterioro?
- Cuáles tienen mayor riesgo de fallar?
- Qué podemos hacer ahora para evitar una parada?

## Criterio de éxito

El sistema debe permitir que un responsable de mantenimiento, sin revisar manualmente grandes cantidades de sensores o múltiples registros históricos, pueda:

1. IDENTIFICAR qué máquinas presentan mayor riesgo de falla.
2. COMPRENDER qué señales o variables justifican ese riesgo.
3. PRIORIZAR qué máquina debería atenderse primero.

## ¿Cómo funciona?

**Datos y Modelo**: Al abrir la aplicación, los datos y el modelo entrenado se descargan automáticamente (para fines de presetación, instancia desde GitHub). El modelo ya viene serializado, entrenado y listo para usar.

**Inferencia (Predicción)**: Cada vez que cargas el dashboard, el modelo analiza los 87,700 registros de 100 máquinas y calcula el riesgo de falla en las próximas 24h para cada una. Se hace en lote (batch) una sola vez, no máquina por máquina.

**Simulador**: Permite "rebobinar" o "avanzar" el reloj hora a hora para ver cómo cambia el riesgo en el tiempo. Tiene controles de reproducción (play/pausa/avance/retroceso) y muestra alertas cuando el riesgo sube/baja.

**Predicción y Alertas**: El modelo asigna 3 niveles: Crítico (≥60%), Moderado (30-59%), Estable (<30%). Las lámparas parpadeantes indican cambios de nivel en tiempo real.

**Priorización y Reporte**: Combina riesgo × criticidad = score de prioridad. Muestra cola ordenada con acción recomendada (Intervenir/Inspeccionar/Monitorear/Ninguna) y plazos. Botón "Reporte" muestra las 5 señales principales que explican el riesgo.

## Alcance MVP

### MUST HAVE

- Dataset seleccionado y justificado ✅ **Azure PdM**
- Limpieza y tratamiento de datos ✅
- EDA ✅
- Modelo ML con baseline, predicción de riesgo y explicabilidad ✅
- Dashboard con resumen, ranking de riesgo, prioridad y detalle de máquina ✅
- Integración, pruebas y deploy ✅

### SHOULD HAVE

- SHAP o explicación avanzada ✅ (Feature importance y señales en UI)
- Filtros avanzados ✅ (Estado de riesgo, criticidad, selectores dinámicos)
- Comparación de máquinas ✅ (Detalle por activo y matriz de riesgo)
- Exportación ✅
- Recomendación preventiva específica ✅ (Acciones y plazos de atención recomendados)

### COULD HAVE

- Alertas visuales dinámicas ✅ (Lámparas parpadeantes y tarjetas animadas según nivel de riesgo)
- Simulador interactivo de telemetría ✅ (Pruebas de resistencia y alteración de sensores en vivo)
- RUL / Horas hasta falla (Documentado en roadmap futuro)
- API independiente (Documentado en arquitectura como decisión futura)

## Flujo de solución

Dataset → Limpieza → Feature Engineering → Modelo ML → Artefacto (.joblib) → Streamlit → Dashboard + Simulador → Decisión

## Arquitectura inicial

- Dataset en `data/` (Azure PdM seleccionado)
- Limpieza y feature engineering en `src/` y `notebooks/`
- Modelo serializado en `models/baseline_model.joblib`
- Dashboard en `dashboard/app.py` (Streamlit + componentes modulares)
- FastAPI: opcional, no es dependencia del MVP

## Stack tecnológico

- Python 3.11+
- Pandas, NumPy
- Scikit-learn
- Joblib
- Plotly / Matplotlib / Seaborn
- Stitch
- Streamlit
- Jupyter / Google Colab
- Git, GitHub
- Deploy: Streamlit Community Cloud

## Roles del equipo

Activos ✅

### Data Analysts

- Lorena Urrutia  ✅
- Héctor García  ✅

Product & Business, historias de usuario, KPIs, criticidad, EDA, visualización, tendencias, Data Quality, profiling, nulos, outliers, reporte ejecutivo, presentación demo.

### Data Scientists

- Lennin Temoche ✅

EDA Predictivo, FeatureEngineering, Modelado,

Pipeline ML, validación, serialización, integración, Dashboard Streamlit, UX.

### Software Engineer

- Albeiro Burbano ✅

Arquitectura, GitHub, integración, deploy, CI

## Estructura del repositorio

- **`data/`** — Datasets (raw y processed)
- **`notebooks/`** — Exploración, ingeniería de features y modelado
- **`src/`** — Código de producción (data, features, models, utils)
- **`models/`** — Artefactos del modelo (`baseline_model.joblib`)
- **`dashboard/`** — Aplicación Streamlit (`app.py`, `components/`, `utils/`)
- **`tests/`** — Pruebas unitarias de estructura y lógica
- **`docs/`** — Documentación técnica, negocio y arquitectura
- **`.github/`** — Templates y workflows de CI (GitHub Actions)
- **`.streamlit/`** — Configuración de Streamlit (theme, server)

## Estado actual

**Core MVP (100% Completado):** Modelo entrenado, serializado e integrado en dashboard Streamlit con tema oscuro premium, simulador interactivo de telemetría y sistema de alertas visuales en vivo. Pipeline ML-Dashboard funcional end-to-end.

**Dataset seleccionado:** Microsoft Azure Predictive Maintenance (Azure PdM) ✅

- Evaluación completada con matriz de 20 criterios ponderados.
- Análisis automatizado en `notebooks/01_data_exploration.ipynb`.
- Documentación en `docs/dataset_selection.md` y `docs/decisions.md` (DEC-009).

**Modelo Candidato (Random Forest):**

- PR-AUC: 0.9919 | ROC-AUC: 0.9999 | Recall: 1.0 | Precision: 0.8001 (threshold=0.5591)
- Threshold guardado en el artefacto: `0.5591`
- 46 features (sensores + historial errores + mantenimiento + rolling windows + deltas)
- Serializado en `models/baseline_model.joblib`

**Split temporal (sin data leakage):**

| Split | Filas   | %      | Periodo                  | Tasa positivos |
| ----- | ------- | ------ | ------------------------ | -------------- |
| Train | 654,600 | 74.72% | 2015-01-01 → 2015-09-30 | 2.01%          |
| Test  | 131,400 | 15.00% | 2015-10-02 → 2015-11-25 | 1.68%          |
| Live  | 87,700  | 10.01% | 2015-11-25 → 2016-01-01 | 1.97%          |

- Gap de 24h entre train y test
- Validación anti-leakage: 4 estrategias confirman PR-AUC > 0.99 (temporal, mensual, por máquina, aleatorio)

**Dashboard (`dashboard/app.py`):** Pipeline de inferencia en tiempo real y componentes avanzados:

- **Carga de datos:** `live_demo.parquet` (87,700 filas, 100 máquinas) desde GitHub (`main/data/processed/`) con fallback local `data/processed/live_demo.parquet`. Cache con `@st.cache_data`.
- **Carga de modelo:** `baseline_model.joblib` desde GitHub (`main/models/`) con fallback local. Cache con `@st.cache_resource`.
- **Selector de origen:** Sidebar con radio `GitHub` / `Local` + botón 🔄 Recargar (limpia caches).
- **Inferencia:** `model.predict_proba()` sobre las 46 features del artefacto; el umbral binario se lee del artefacto.
- **Componentes clave:**
  - `demo_simulator.py`: Simulador interactivo de telemetría y pruebas de resistencia/anomalías.
  - `risk_table.py`: Matriz interactiva de riesgo con lámparas luminosas parpadeantes por nivel de criticidad.
  - `machine_detail.py`: Diagnóstico individualizado por activo y recomendaciones de intervención.
  - `sensor_chart.py`: Gráficos de tendencias temporales de sensores.

**Tests:** 7/7 passing (`tests/`)

- Mejoras de calidad de código: Corrección de indentación y eliminación de fragmentos duplicados en `dashboard/components/demo_simulator.py` y `dashboard/app.py` sin cambios funcionales.

**MVP completado:**

- UI/UX refinada con Stitch (tema, componentes, responsive)
- Deploy a Streamlit Cloud / CI/CD rebuild automático
- Streaming tiempo real / Monitoreo drift en producción
- SHAP explainability (opcional)

## Próximos pasos y evolución de arquitectura

### Mejoras Inmediatas (Corto plazo)

- **Entrenar otros modelos**: como LSTM, CatBoost, CNN, Redes Neuronales, etc. con el objetivo de compararlos con el modelo actual y determinar cuál es el más eficiente, considerar hibridación.
- **CI/CD automático**: GitHub Actions para rebuild del modelo y deploy a Streamlit Cloud
- **Monitoreo de drift**: Alertas si la distribución de features cambia en producción
- **SHAP explainability**: Explicaciones por predicción individual (no solo feature importance global)

### Escalabilidad y Arquitectura (Mediano plazo)

- **FastAPI + Autenticación**: API REST separada del dashboard para:
  - Autenticación/autorización (JWT, roles: admin, operador, viewer)
  - Endpoints: `/predict`, `/risk-ranking`, `/machine-detail`, `/telemetry`
  - Base de datos PostgreSQL para historial de predicciones, auditoría, configuración
- **Alertas persistentes**: Sistema de notificaciones (email, Slack, Teams, móvil) con reglas configurables
- **Multi-tenancy**: Soporte para múltiples plantas/clientes en una sola instancia

### Migración de Frontend (Largo plazo)

**Objetivo**: Migrar de Streamlit (Python) a React 18 SPA para mayor control UX, performance y escalabilidad.

| Aspecto   | Actual (Streamlit)       | Objetivo (React 18 SPA)                                                    |
| --------- | ------------------------ | -------------------------------------------------------------------------- |
| Runtime   | Python (servidor)        | Navegador (Web)                                                            |
| Framework | Streamlit                | React 18 + Vite + TypeScript + Tailwind CSS                                |
| Estado    | Server-side session      | Client-side (Zustand/Redux) + React Query                                  |
| Gráficos | Plotly (server-rendered) | Recharts / Visx / uPlot (client-side)                                      |
| Real-time | `@st.fragment` polling | WebSockets / Server-Sent Events                                            |
| Deploy    | Streamlit Cloud          | Vercel / Netlify / Azure Static Web Apps + FastAPI en Azure Container Apps |

**Componentes a migrar**:

1. `risk_table.py` → Tabla virtualizada con ordenamiento/filtrado client-side
2. `sensor_chart.py` → Gráficos interactivos con zoom/pan/brush nativo
3. `demo_simulator.py` → Controles de reproducción + WebSocket para tiempo real
4. `machine_detail.py` → Vista detalle con pestañas, accordion, lazy loading
5. `mini_report.py` → Modal/panel lateral con feature importance interactivo
6. Auth: Login page, protected routes, role-based UI

**Backend (FastAPI) endpoints necesarios**:

```
GET  /api/v1/machines                    # Lista máquinas con risk_score
GET  /api/v1/machines/{id}/risk          # Detalle riesgo + señales
GET  /api/v1/machines/{id}/telemetry     # Serie temporal (con query params: period, from, to)
GET  /api/v1/machines/{id}/errors        # Histórico errores
GET  /api/v1/simulation/state            # Estado simulador (time, running, period)
POST /api/v1/simulation/control          # play/pause/step/reset
GET  /api/v1/report/{machine_id}         # Mini-reporte (feature importance, root cause)
WS   /ws/simulation                      # Updates en tiempo real (0.8s)
```

**Criterios de migración**:

- Paridad funcional 100% antes de switch
- Mantener modelo Python (joblib) servido vía FastAPI
- Tests E2E (Playwright) para validar paridad visual/comportamiento
- Deploy canary / feature flags para rollout gradual

## Roadmap de 4 semanas

- Semana 1: Discovery + Dataset + Data Foundation + EDA inicial + dashboard skeleton
- Semana 2: ML + integración inicial
- Semana 3: Producto (ranking, criticidad, explicabilidad)
- Semana 4: Testing + Deploy + Demo

Ver docs/roadmap.md para el calendario detallado.

## Backlog

Ver docs/backlog.md para el backlog completo organizado por épicas.

## Reglas de desarrollo

- Crear branch feature/<id></id>-descripcion, fix/<id></id>- descripcion, docs/< descripcion>
- Commits con prefijo: feat:, fix:, docs:, refactor:, test:, chore:
- PR por tarea, con al menos un revisor
- Definition of Done: desarrollada, funciona, probada, revisada, integrada, documentada

## Cómo preparar el entorno local

### Requisitos

- Python 3.12 o superior
- Git
- IDE con terminal integrada (VS Code, Antigravity, etc.)

### Paso 1: Clonar

```bash
git clone https://github.com/No-Country-simulation/S08-26-EQUIPO-24
cd S08-26-EQUIPO-24
```

### Paso 2: Crear entorno virtual

```bash
python -m venv .venv
```

### Paso 3: Activar

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# Linux/macOS
source .venv/bin/activate
```

### Paso 4: Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se requiere Python 3.11 o superior. `scikit-learn` queda fijado a la version usada para serializar el modelo.

### Paso 5: Verificar

```bash
python -c "import pandas, pyarrow, streamlit, sklearn; print('OK')"
```

### Paso 6: Ejecutar

```bash
# Notebook
jupyter notebook notebooks/

# Dashboard
streamlit run dashboard/app.py
```

> Ver `CONTRIBUTING.md` para pasos detallados y solución de problemas.

## Cómo ejecutar el dashboard

```bash
streamlit run dashboard/app.py
```

### Estado actual del dashboard

- **Datos:** `live_demo.parquet` (87,700 filas, 100 máquinas, 46 features + target) desde GitHub `main/data/processed/` con fallback local.
- **Modelo:** `baseline_model.joblib` (Random Forest, 2.50 MB) desde GitHub `main/models/` con fallback local.
- **Carga dual:** Sidebar con selector `GitHub` / `Local` + botón 🔄 Recargar (limpia `st.cache_data` y `st.cache_resource`, fuerza rerun).
- **Riesgo por máquina:** Se muestra la probabilidad de falla de la última lectura disponible. Las predicciones binarias respetan el umbral guardado en el artefacto; no se fuerza una cantidad fija de positivos.
- **UI/UX:** Completa e interactiva con tema dark premium, componentes modulares, simulador de telemetría y alertas animadas.
- **Decisiones:** El responsable de mantenimiento ve ranking de riesgo, señales (telemetría + errores), prioridad, plazos recomendados y recomendación de intervención (Intervenir/Inspeccionar/Monitorear/Ninguna).

## Cómo contribuir

Ver CONTRIBUTING.md.

## Limitaciones conocidas

- El artefacto del modelo puede mostrar `InconsistentVersionWarning` si la versión de scikit-learn no coincide con la de entrenamiento (1.7.2 vs 1.9.1 actual); se recomienda regenerarlo en el entorno objetivo.
- FastAPI inicialmente no está incluido en el MVP.
- Dataset AI4I 2020 solo para validación secundaria.

## Nota sobre datasets

Dataset principal: **Azure PdM** en `data/raw/` (5 archivos). Validación secundaria: AI4I 2020.
Los datos crudos van en data/raw/ y no se modifican.

## Principio de transparencia

Crear variables derivadas es válido cuando existe justificación técnica o de negocio y el proceso es reproducible. No se deben inventar datos históricos.

## Demo de la Aplicación

🔗 **App en vivo:** https://s08-26-equipo-24git-g3stte6g7k8tr9wbnrichu.streamlit.app/

El pipeline core (datos → modelo → inferencia → UI + simulador) está 100% funcional. También se puede ejecutar localmente:

```bash
streamlit run dashboard/app.py
```

El dashboard permite al responsable de mantenimiento:

1. **Identificar** máquinas con mayor riesgo (ranking interactivo + bar chart + alertas críticas luminosas).
2. **Comprender** señales (telemetría temporal volt/rotate/pressure/vibration + histórico de errores + simulador de anomalías).
3. **Priorizar** intervención (cola ordenada por `priority_score` = riesgo × criticidad + recomendación principal + plazos de atención).

---

**Contacto:**

**Proyecto: Predictive Maintenance**

**EQUIPO NO COUNTRY SET-2026: S08-26-EQUIPO-24**

* [lurquijon@gmail.com](mailto:lurquijon@gmail.com)
* [hdgh2355@gmail.com](mailto:hdgh2355@gmail.com)
* [albeirojbt@gmail.com](mailto:albeirojbt@gmail.com)
* [bigo42923@gmail.com](mailto:bigo42923@gmail.com)

---

## Licencia

Este proyecto está bajo la **Licencia MIT**. Puedes usar, modificar y distribuir el código libremente, siempre y cuando se mantenga el aviso de derechos de autor y se mencione el repositorio original y a sus autores.

---

