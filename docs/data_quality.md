# Documentación --- Fase 2: Data Cleaning, Data Quality e Integración EDA

## Proyecto: PredictiveMaintenance — Sistema de Mantenimiento Predictivo Industrial

**No Country --- S08-26 Equipo 24**
**Dataset:** Azure Predictive Maintenance (Azure PdM)
**Rol:** ML Pipeline & Integration
**Notebook:** `02_data_cleaning_EDA_integrado.ipynb`

## 1. Objetivo

Validar la calidad e integridad de las cinco fuentes de Azure PdM y
construir una base temporal unificada para EDA predictivo, Feature
Engineering y Machine Learning.

Se revisaron estructura, tipos, fechas, identificadores, nulos,
duplicados, rangos, consistencia temporal e integración entre tablas.

## 2. Fuentes de datos

Fuente Registros Propósito

---

`PdM_telemetry.csv` 876,100 Telemetría horaria
`PdM_errors.csv` 3,919 Registro de errores
`PdM_failures.csv` 761 Historial de fallas
`PdM_maint.csv` 3,286 Historial de mantenimiento
`PdM_machines.csv` 100 Características de las máquinas

## 3. Calidad de datos

Las columnas `datetime` fueron convertidas a tipo temporal de pandas.

No se encontraron filas completamente duplicadas en ninguna de las cinco
fuentes.

La telemetría contiene 876,100 registros, 100 máquinas y no presenta
valores nulos en sus variables principales. Promedios: voltaje 170.78 V,
rotación 446.61 RPM, presión 100.86 psi y vibración 40.39 m/s².

El mantenimiento contiene 3,286 registros distribuidos entre `comp1`
(804), `comp2` (863), `comp3` (808) y `comp4` (811).

## 4. Aportes integrados

### EDA Descriptivo - Lorena

Se incorporaron como complemento del flujo principal: - Distribuciones
de sensores. - Actividad de mantenimiento por máquina. - Visualización
de relación entre errores y fallas. - Heatmap de correlaciones de
telemetría.

### Análisis Ejecutivo - Héctor

El análisis ejecutivo muestra:

- 100 máquinas
- Distribución por modelo
- Edad promedio de 11.33 años, rango 0--20
- 3,919 errores
- 761 fallas
- 3,286 mantenimientos
- Máquinas con mayor recurrencia de errores y fallas
- Resumen del comportamiento de sensores

La correlación de Pearson entre total de errores y total de fallas por
máquina es aproximadamente **r = 0.54**, una asociación positiva
moderada. Esto se interpreta como relación estadística, no como
causalidad.

## 5. Dataset Maestro `master_dataset.parquet`

La telemetría se utiliza como eje temporal y se integran características
estáticas, errores y mantenimiento.

### Variables de telemetría

- `volt`
- `rotate`
- `pressure`
- `vibration`

### Máquina

- `model`
- `age`

### Errores

- `errors_last_24h`
- `errors_last_7d`
- `distinct_errors_last_24h`
- `time_since_last_error_h`
- `has_error_recent`

### Mantenimiento

- `hours_since_maintenance`
- `days_since_maintenance`
- `maintenance_count_30d`
- `time_since_last_component_replacement_h`
- `has_recent_maintenance`

Las variables históricas respetan la disponibilidad temporal de la
información y se evita utilizar eventos futuros como predictores.

## 6. Variable objetivo - Target

Se construyó `failure_next_24h`:

- `1`: ocurre una falla en el intervalo **(t, t + 24h)**.
- `0`: no se registra una falla en ese intervalo.

Resultado: - Total: **876,100** - Positivos: **17,184** - Negativos:
**858,916** - Positivos: **1.96%** - Máquinas sin positivos: **2 de
100**

El desbalance de clases deberá considerarse en la etapa de modelado.

Se validó además la sensibilidad a otros horizontes: 48h = 3.88%, 72h =
5.79% y 7 días = 13.36%. El horizonte de 24h queda como candidato de
trabajo y deberá confirmarse en el EDA predictivo.

También se identificó censura por la derecha: 2,400 filas corresponden a
las últimas 24h de las series y no tienen futuro observable dentro del
dataset.

## 7. Hallazgos para Machine Learning

Existe una asociación positiva entre recurrencia de errores y fallas.
Las máquinas 22 y 99 destacan tanto por volumen de errores como por
número de fallas.

Sin embargo, el análisis no demuestra que un error aislado provoque una
falla. La siguiente fase debe estudiar frecuencia, recencia y evolución
temporal.

Los cuatro sensores presentan correlaciones lineales prácticamente nulas
entre sí. Por tanto, no se establece un umbral de falla basado
únicamente en una lectura instantánea.

El foco predictivo debe analizar: - Tendencias temporales. - Cambios
respecto al comportamiento habitual. - Ventanas previas a una falla. -
Variabilidad de sensores. - Errores recientes. - Historial de
mantenimiento. - Antigüedad y modelo de máquina.

## 8. Entregable

Se generó:

`master_dataset.parquet` en la carpeta `data/interim/`

El dataset conserva **876,100 filas** y constituye la base reproducible
para EDA predictivo y Feature Engineering.

## 9. Checklist de salida

- ✅ Cinco fuentes validadas.
- ✅ Fechas convertidas.
- ✅ `machineID` validado.
- ✅ Sin duplicados completos.
- ✅ Nulos revisados.
- ✅ Integración temporal documentada.
- ✅ Sin multiplicación indebida de filas.
- ✅ Variables históricas respetando el tiempo.
- ✅ Target inicial construido.
- ✅ Desbalance cuantificado.
- ✅ `master_dataset.parquet` generado.
- ⚠️ El horizonte definitivo del target debe confirmarse en EDA
  predictivo.

## 10. Próxima fase

Fase EDA predictivo - deberá responder a:

> **¿Qué señales o comportamientos aparecen antes de una falla?**

El siguiente EDA predictivo deberá comparar períodos normales y períodos
previos a falla, analizar tendencias temporales, errores, mantenimiento,
comportamiento por máquina/modelo y definir las variables que pasarán al
Feature Engineering y al pipeline de Machine Learning.

## 11. Conclusión

La conclusión de esta fase deja una base consistente y reproducible. Las cinco
fuentes ya están integradas alrededor de `machineID` y `datetime`, integradas con variables estáticas, errores, mantenimiento y se dispone de un target inicial.

El siguiente paso de ML consiste en descubrir qué comportamiento precede
realmente a una falla, evitando asumir que una lectura instantánea o una
correlación aislada constituye por sí sola una señal predictiva.
