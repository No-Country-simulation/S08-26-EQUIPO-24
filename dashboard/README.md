# Dashboard PredictiveMaintenance

Instrucciones y Documentación Técnica (Español)

## Propósito
Aplicación Streamlit interactiva para la visualización de riesgos, telemetría y simulación de anomalías en tiempo real basada en el modelo de Machine Learning (`models/baseline_model.joblib`) y el dataset procesado (`data/processed/live_demo.parquet`).

## Componentes del Dashboard

- **`dashboard/app.py`**: Punto de entrada de la aplicación, manejo de layout global, tema oscuro premium CSS y enrutamiento de pestañas.
- **`dashboard/components/demo_simulator.py`**: Simulador de telemetría y pruebas de anomalías en vivo. Permite reproducir eventos históricos y alterar lecturas de sensores para evaluar la respuesta del modelo ML.
- **`dashboard/components/risk_table.py`**: Matriz de riesgo interactiva con sistema de alertas luminosas animadas (`alert-lamp`) y cálculo de plazos de atención operativa.
- **`dashboard/components/machine_detail.py`**: Vista diagnóstica detallada por máquina con metadatos del activo y recomendaciones preventivas.
- **`dashboard/components/sensor_chart.py`**: Gráficos de series temporales para monitoreo de voltaje, rotación, presión y vibración.
- **`dashboard/utils/data_loader.py`**: Carga de datos reales (`live_demo.parquet`) desde GitHub (`main`) o local con cache `@st.cache_data`.
- **`dashboard/utils/model_loader.py`**: Carga del artefacto del modelo (`baseline_model.joblib`) desde GitHub (`main`) o local con cache `@st.cache_resource`.

## Requisitos
- Python 3.11+
- Virtualenv / venv activo
- Dependencias instaladas desde `requirements.txt` (`pip install -r requirements.txt`).

## Ejecutar localmente
1. Activar entorno virtual (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Modo de origen (GitHub / Local)
- En la barra lateral superior está el selector `Origen de datos`:
  - `GitHub`: Descarga `live_demo.parquet` y `baseline_model.joblib` desde la rama `main` de GitHub.
  - `Local`: Carga directamente los archivos locales (`data/processed/live_demo.parquet` y `models/baseline_model.joblib`), ideal para desarrollo offline.

## Recargar artefactos
- Utiliza el botón `🔄 Recargar modelo y datos` en la barra lateral para vaciar las memorias cache (`st.cache_data` y `st.cache_resource`) y forzar la recarga inmediata de los datos y el modelo.

## Características Destacadas
- **Alertas luminosas dinámicas:** Lámparas parpadeantes en color rojo para nivel *Crítico*, naranja para *Moderado* y verde para *Estable*.
- **Plazos de atención recomendados:** Recomendaciones de mantenimiento y plazos de atención operativa calculados a partir de la prioridad ponderada (`risk_score` × `criticality`).
- **Simulador de anomalías:** Herramienta interactiva para experimentar en tiempo real con cambios en las variables de telemetría.
- **Ranking determinista:** Evaluación de riesgo basada en la lectura más reciente de cada activo.

## Advertencia de versión de scikit-learn
- Al cargar `baseline_model.joblib` puede surgir la advertencia `InconsistentVersionWarning` si la versión local de `scikit-learn` difiere de la versión de entrenamiento (1.7.2). El código gestiona esto de forma segura.

## Contacto
- Equipo S08-26-EQUIPO-24

