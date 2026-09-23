# Guion de demo

Este documento es el guion para la demostración del MVP.

**IMPORTANTE:** Aún no existe el producto. Este es el guion para cuando esté listo.

---

## Objetivo de la demo

Demostrar que el sistema permite a un responsable de mantenimiento:

1. Identificar máquinas con mayor riesgo.
2. Comprender las señales del riesgo.
3. Priorizar qué atender primero.

---

## Flujo de demo

### 1. Contexto
- Problema: paradas imprevistas, análisis manual de sensores.
- Solución: mantenimiento predictivo.

### 2. Dashboard general
- Resumen de estado de máquinas.
- Ranking de riesgo.

### 3. Identificar riesgo
- Seleccionar la máquina con mayor riesgo.
- Mostrar score.

### 4. Comprender riesgo
- Señales relevantes.
- Tendencias.

### 5. Priorizar
- Combinar riesgo y criticidad.
- Mostrar prioridad.

### 6. Acción
- Recomendación de intervención.

---

## Estado actual

**✅ COMPLETADO - Dashboard e Integración ML Funcionando**

---

## Plan de Integración: Modelo ML + Live Demo → Dashboard Streamlit

### Resumen del Estado Actual

| Componente | Estado | Ubicación |
|------------|--------|-----------|
| Notebook modelado | ✅ Completado | `notebooks/05_modeling.ipynb` |
| Modelo serializado | ✅ En GitHub | `feat/modeling_integration/models/baseline_model.joblib` |
| Live demo data | ✅ En GitHub | `feat/feature_engineering/data/processed/live_demo.parquet` |
| Dashboard skeleton | ✅ Existente | `dashboard/` |
| Model loader | ✅ Funcional | `dashboard/utils/model_loader.py` |
| Data loader | ✅ Nuevo | `dashboard/utils/data_loader.py` (carga real de datos) |

---

## Verificación del Notebook (05_modeling.ipynb) ✅

### ✅ Conforme
- **Split temporal correcto**: 75% train / 15% test / 10% live con gap de 24h
- **live_df exportado**: `data/processed/live_demo.parquet` (87,700 filas, 100 máquinas)
- **Modelo guardado**: `models/baseline_model.joblib` con Random Forest, 46 features, threshold optimizado (0.42)
- **Artefacto completo**: Incluye model, feature_cols, decision_threshold, métricas, metadatos temporales
- **Validación anti-leakage**: 4 splits confirmados (temporal, mensual, por máquina, aleatorio) → PR-AUC > 0.99 en todos

### ⚠️ Observaciones Menores
- El scaler **no** se guarda en el joblib (RF no lo necesita) → `model_loader.py` lo maneja correctamente
- `feature_cols` = 46 features (excluye datetime, machineID, failure_next_24h)
- Target `failure_next_24h` balanceado en train/test/live

---

## Plan de Implementación

### FASE 1: Carga de Datos Reales (data_loader.py)

**Objetivo**: Reemplazar `load_mock_data()` por carga real desde GitHub/local

1. **`load_live_demo_data()`** - Carga live_demo.parquet desde GitHub con fallback local + cache 1h
2. **`load_machines_from_live()`** - Extrae metadatos únicos de máquinas desde live_df
3. **`compute_risk_from_model()`** - Ejecuta inferencia del modelo sobre live_df y retorna df_risk + metadatos

### FASE 2: Integración en app.py

- Reemplazar `load_mock_data()` por carga real
- Integrar meta del modelo en UI (sidebar: fuente, PR-AUC, threshold, fechas train/test)

### FASE 3: Componentes - Adaptación a Datos Reales

| Componente | Cambio Requerido |
|------------|------------------|
| `risk_table.py` | Usar `df_risk` real (machine_id, risk_score, risk_level, criticality, priority) |
| `sensor_chart.py` | Filtrar `df_telemetry` por machine_id, usar timestamps reales |
| `machine_detail.py` | Mostrar error_code/description reales de `df_errors` |
| `priority_list.py` | Ordenar por `priority_score` real (riesgo × criticidad) |

### FASE 4: Validación y Pruebas

```bash
cd dashboard && streamlit run app.py
```
- [ ] Modelo carga desde GitHub (fallback local OK)
- [ ] live_demo.parquet carga (87k filas, cache 1h)
- [ ] 100 máquinas con risk_score real
- [ ] Telemetría temporal real
- [ ] Errores históricos reales
- [ ] Sidebar expone PR-AUC, threshold, fechas train/test

---

## Archivos a Modificar

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `dashboard/utils/data_loader.py` | **Modificar** | Añadir `load_live_demo_data()`, `load_machines_from_live()`, `compute_risk_from_model()` |
| `dashboard/app.py` | **Modificar** | Reemplazar mock data por carga real, integrar meta del modelo en UI |
| `dashboard/components/risk_table.py` | **Revisar** | Asegurar compatibilidad con columnas reales |
| `dashboard/components/sensor_chart.py` | **Revisar** | Usar datetime real, no índice sintético |
| `dashboard/components/machine_detail.py` | **Revisar** | Mostrar error_code/description reales |
| `dashboard/components/priority_list.py` | **Revisar** | Usar priority_score calculado |

---

## Dependencias y Riesgos

| Riesgo | Mitigación |
|--------|------------|
| GitHub rate limit / caída | Fallback local ya implementado en `model_loader.py`; replicar en `data_loader.py` |
| Columnas feature mismatch | Validación estricta en `predict_probabilities()` + logging claro |
| live_demo.parquet grande (~87k filas) | Cache `@st.cache_data(ttl=3600)` en loader |
| Zona horaria datetime | Asegurar `pd.to_datetime(..., utc=True)` en carga |

---

## Próximos Pasos (Out of Scope)

- [ ] Hyperparameter tuning (actualmente Random Forest optimizado)
- [ ] Cost-sensitive threshold selection (threshold 0.42 optimizado)
- [ ] SHAP explainability (feature importance documentada)
- [ ] Deploy a Streamlit Cloud / Azure Container Apps
- [ ] CI/CD para rebuild automático del modelo

---

## Criterios de Aceptación

1. **Dashboard carga sin mock data**: `load_mock_data()` ya no se usa en `app.py`
2. **Modelo desde GitHub**: Logs muestran `source: "GitHub (feat/modeling_integration)"`
3. **Live demo visible**: 100 máquinas con risk_score basado en inferencia real
4. **Telemetría temporal**: Gráficos usan `datetime` real de live_df
5. **Errores reales**: Tabla de errores muestra códigos/descripciones de live_df
6. **Métricas expuestas**: Sidebar muestra PR-AUC, threshold, fechas train/test

---

## Plan de Integración: Modelo ML + Live Demo → Dashboard Streamlit

### Resumen del Estado Actual

| Componente | Estado | Ubicación |
|------------|--------|-----------|
| Notebook modelado | ✅ Completado | `notebooks/05_modeling.ipynb` |
| Modelo serializado | ✅ En GitHub | `feat/modeling_integration/models/baseline_model.joblib` |
| Live demo data | ✅ En GitHub | `feat/feature_engineering/data/processed/live_demo.parquet` |
| Dashboard skeleton | ✅ Existente | `dashboard/` |
| Model loader | ✅ Funcional | `dashboard/utils/model_loader.py` |
| Data loader | ⚠️ Solo mock | `dashboard/utils/data_loader.py` |

### Verificación del Notebook (05_modeling.ipynb) ✅

- **Split temporal correcto**: 75% train / 15% test / 10% live con gap de 24h
- **live_df exportado**: `data/processed/live_demo.parquet` (87,700 filas, 100 máquinas)
- **Modelo guardado**: `models/baseline_model.joblib` con Random Forest, 46 features, threshold optimizado
- **Artefacto completo**: Incluye model, feature_cols, decision_threshold, métricas, metadatos temporales
- **Validación anti-leakage**: 4 splits confirmados (temporal, mensual, por máquina, aleatorio) → PR-AUC > 0.99 en todos

### Plan de Implementación

#### FASE 1: Carga de Datos Reales (data_loader.py)

**Objetivo**: Reemplazar `load_mock_data()` por carga real desde GitHub/local

1. **`load_live_demo_data()`** - Carga live_demo.parquet desde GitHub con fallback local + cache 1h
2. **`load_machines_from_live()`** - Extrae metadatos únicos de máquinas desde live_df
3. **`compute_risk_from_model()`** - Ejecuta inferencia del modelo sobre live_df y retorna df_risk

#### FASE 2: Integración en app.py

- Reemplazar `load_mock_data()` por carga real
- Integrar meta del modelo en UI (sidebar: fuente, PR-AUC, threshold, fechas train/test)

#### FASE 3: Componentes - Adaptación a Datos Reales

| Componente | Cambio Requerido |
|------------|------------------|
| `risk_table.py` | Usar `df_risk` real |
| `sensor_chart.py` | Usar datetime real, no índice sintético |
| `machine_detail.py` | Mostrar error_code/description reales |
| `priority_list.py` | Usar priority_score calculado |

#### FASE 4: Validación y Pruebas

```bash
cd dashboard && streamlit run app.py
```
- [ ] Modelo carga desde GitHub (fallback local OK)
- [ ] live_demo.parquet carga (87k filas, cache 1h)
- [ ] 100 máquinas con risk_score real
- [ ] Telemetría temporal real
- [ ] Errores históricos reales
- [ ] Sidebar expone PR-AUC, threshold, fechas train/test

### Archivos a Modificar

1. `dashboard/utils/data_loader.py` (principal - FASE 1)
2. `dashboard/app.py` (FASE 2)
3. `dashboard/components/*.py` (FASE 3 - revisar compatibilidad)

### Riesgos y Mitigación

| Riesgo | Mitigación |
|--------|------------|
| GitHub rate limit / caída | Fallback local (replicar patrón de model_loader.py) |
| Columnas feature mismatch | Validación estricta en `predict_probabilities()` + logging claro |
| live_demo.parquet grande (~87k filas) | Cache `@st.cache_data(ttl=3600)` en loader |
| Zona horaria datetime | Asegurar `pd.to_datetime(..., utc=True)` en carga |