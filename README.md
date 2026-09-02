# S08-26-EQUIPO-24

¡Claro! Te lo dejo convertido a Markdown, manteniendo el contenido y mejorando únicamente la estructura, tablas, listas y bloques de código para que puedas guardarlo directamente como .md.

Predictive Maintenance MVP — Propuesta de Proyecto

Con esta definición ya podemos plantear el proyecto como un MVP de Predictive Maintenance, y distribuir el trabajo entre 4 Data Analysts, 1 Data Scientist y 1 Software Engineer sin que todo termine dependiendo del DS.

Mi recomendación como PM es no empezar intentando predecir todas las fallas de todas las máquinas. Primero construiría un pipeline completo sobre un subconjunto de máquinas/componentes y demostraría que podemos pasar de:

Datos → Riesgo → Explicación → Acción

1. Objetivo del MVP

El MVP debería responder cuatro preguntas:

¿Qué máquinas están mostrando comportamiento anómalo?
¿Qué probabilidad tienen de presentar una falla en un horizonte definido?
¿Qué variables/señales explican ese riesgo?
¿Qué máquinas deberían priorizarse para una intervención?

El flujo sería:

Sensores + mantenimiento
          ↓
Calidad / Feature Engineering
          ↓
Anomalías
          ↓
Modelo de riesgo
          ↓
Score de criticidad
          ↓
Dashboard / Alerta
          ↓
Decisión de mantenimiento

2. Distribución propuesta del equipo

Yo organizaría al equipo de la siguiente manera:

Rol	Responsabilidad principal	Foco
DA1	Data & Business Analyst	Entendimiento del negocio, KPIs, criticidad
DA2	Data Quality & Sensor Analyst	Calidad, exploración y comportamiento de sensores
DA3	Maintenance Data Analyst	Historial de mantenimiento y definición de eventos/fallas
DA4	Analytics & Visualization Analyst	Features, análisis exploratorio y dashboard
Data Scientist	Predictive Modeling Lead	Anomalías, predicción, evaluación y modelo
Software Engineer	Data/ML Platform	Pipeline, APIs, integración y deployment

La idea importante es que los 4 DAs alimenten al DS con datasets, definiciones y análisis preparados, mientras el SE construye la infraestructura necesaria para que el resultado pueda convertirse en producto.

3. DA1 — Business & Data Analyst
Misión

Convertir el problema de mantenimiento en requerimientos medibles.

Tareas
Identificar stakeholders:
mantenimiento
producción
operaciones
ingeniería
Definir qué significa una falla.
Definir qué significa:
máquina crítica
máquina bajo observación
máquina de alto riesgo
intervención prioritaria
Identificar KPIs de negocio:
downtime
costo de reparación
número de fallas
MTBF
MTTR
costo de mantenimiento
Definir horizonte de predicción:
por ejemplo, riesgo de falla en próximos 7/14/30 días.
Definir criterios de éxito del MVP.
Construir matriz de criticidad de máquinas.
Traducir el output del modelo a una lógica de priorización para mantenimiento.
Entregables

DA1 →

Business Requirements Document
Data Dictionary de negocio
Definición de falla/evento
Matriz de criticidad
KPIs
Reglas de priorización
Acceptance Criteria
Dependencia

DA1 debería trabajar desde el día 1 con el responsable de mantenimiento.

4. DA2 — Data Quality & Sensor Analyst
Misión

Entender si los datos de sensores realmente pueden utilizarse para detectar deterioro.

Tareas
Inventario de sensores.
Identificar:
frecuencia de medición
unidades
rangos
missing values
outliers
duplicados
gaps temporales
Analizar calidad por máquina.
Analizar distribución de:
temperatura
vibración
presión
velocidad
consumo
ciclos
Detectar sensores defectuosos.
Analizar cambios de comportamiento.
Identificar patrones previos a eventos de mantenimiento.
Investigar correlaciones entre variables.
Generar baseline de comportamiento normal.
Entregables

DA2 →

Sensor Data Quality Report
Dataset limpio de sensores
Data profiling
Baseline de comportamiento
Lista de variables candidatas
Reglas de calidad
Especial atención

DA2 debería trabajar estrechamente con el Data Scientist, porque aquí se empieza a definir qué señales pueden convertirse en features.

5. DA3 — Maintenance Data Analyst

Este rol es especialmente importante.

Misión

Transformar el historial de mantenimiento en labels/eventos utilizables por Machine Learning.

Tenemos que resolver algo fundamental:

¿Qué significa exactamente que una máquina "falló"?

Por ejemplo, no necesariamente:

maintenance_record = failure


Puede haber:

mantenimiento preventivo
inspección
lubricación
cambio de pieza
reparación
falla
emergencia
ajuste
calibración
Tareas
Analizar histórico de mantenimiento.
Clasificar tipos de intervención.
Identificar verdaderas fallas.
Identificar componentes afectados.
Construir timeline por máquina.

Ejemplo:

Machine A

01/01 → Normal
05/01 → Maintenance
12/01 → Increasing vibration
15/01 → Alarm
17/01 → Failure
18/01 → Bearing replacement

Relacionar:
sensores
alarmas
mantenimiento
fallas
componentes
Construir dataset de eventos.
Analizar frecuencia de fallas.
Analizar tiempo entre fallas.
Identificar componentes con mayor recurrencia.
Entregables

DA3 →

Maintenance Event Dataset
Failure Label Definition
Failure Taxonomy
Machine Failure Timeline
Component Failure Analysis
Dataset para entrenamiento

Este trabajo es probablemente uno de los mayores cuellos de botella del proyecto, por lo que asignaría bastante capacidad de DA3 inicialmente.

6. DA4 — Analytics & Visualization Analyst
Misión

Convertir los datos preparados en insights y visualizaciones accionables.

Tareas
EDA integrado.
Crear vistas por máquina.
Crear tendencias de sensores.
Analizar comportamiento pre-falla.
Crear variables agregadas como:
media móvil
desviación estándar
máximo/mínimo
tendencia
tasa de cambio
rolling statistics
Diseñar mockups del dashboard.
Definir UX para mantenimiento.
Construir dashboard MVP.
Visualizar:
Risk Score
criticidad
tendencia
últimas alarmas
mantenimiento
fallas
señales relevantes
Entregables

DA4 →

EDA integrado
Feature candidates
Dashboard prototype
Risk visualization
Machine detail view
Maintenance prioritization view

DA4 debería comenzar el diseño del dashboard antes de tener el modelo terminado, no después.

7. Data Scientist
Misión

Desarrollar el motor predictivo.

El DS no debería encargarse de limpiar todo el dataset ni de construir el dashboard.

Su tiempo debe concentrarse en el problema de ML.

Fase 1 — Baseline

Antes de un modelo complejo:

baseline histórico
reglas simples
threshold de sensores
anomaly detection básico

Ejemplo:

IF vibration > threshold
AND temperature trend increasing
THEN elevated risk


Esto permite comparar posteriormente contra ML.

Fase 2 — Feature Engineering

Con apoyo de DA2 y DA3:

rolling mean
rolling std
trend
rate of change
sensor interactions
time since maintenance
operating hours
cycles
previous failures
component age
Fase 3 — Modelos

Dependiendo de la cantidad/calidad de datos:

Supervised
Logistic Regression
Random Forest
XGBoost / LightGBM
Unsupervised / Anomaly Detection
Isolation Forest
clustering
autoencoders, si realmente están justificados
Survival / Remaining Useful Life

Podría evaluarse posteriormente:

Survival Analysis
Cox models
RUL models

Pero no lo pondría como requisito del MVP.

Fase 4 — Evaluación

Muy importante: no evaluar solamente accuracy.

Medir:

Precision
Recall
F1
PR-AUC
False Negatives
False Positives
Lead Time

Especialmente:

¿Cuánto tiempo antes de la falla conseguimos detectar el deterioro?

Fase 5 — Explainability

El mantenimiento debe poder entender:

"¿Por qué esta máquina tiene riesgo alto?"

Por eso el DS debería entregar:

principales features
contribution de variables
tendencias relevantes
explicación del score
Entregables

DS →

Baseline
Feature dataset
Anomaly detection
Predictive model
Model evaluation
Risk score
Explainability
Model artifact
Inference specification
8. Software Engineer
Misión

Convertir el análisis/modelo en un sistema ejecutable y mantenible.

Tareas
Data Ingestion

Construir ingestion para:

Sensor data
      ↓
Raw data
      ↓
Processed data
      ↓
Feature data

Data Pipeline

Automatización de:

ingestion
transformación
validación
feature generation
scoring
ML Integration

Integrar el modelo del DS:

New sensor data
      ↓
Pipeline
      ↓
Features
      ↓
ML model
      ↓
Risk Score

Backend

API para consultar:

machine
current status
risk score
alerts
historical trends
explanations
Frontend Integration

Si el MVP requiere aplicación web:

Dashboard
    ↓
API
    ↓
Prediction service
    ↓
Data / ML layer

Deployment
environment
CI/CD
logging
monitoring
model versioning
error handling
Entregables

SE →

Data pipeline
Feature pipeline
Model serving
API
Backend
Deployment
Monitoring básico
Integration con dashboard
9. Cómo repartiría las fases

Propongo 6 fases.

Fase 1 — Discovery & Data Assessment
Objetivo

Saber si tenemos datos suficientes para hacer el proyecto.

Persona	Carga
DA1	80%
DA2	100%
DA3	100%
DA4	50%
DS	30%
SE	20%

DA1 define negocio.

DA2 analiza sensores.

DA3 analiza mantenimiento.

DS evalúa factibilidad ML.

SE entiende fuentes e infraestructura.

10. Fase 2 — Data Foundation
Objetivo

Construir datasets confiables.

Persona	Carga
DA1	40%
DA2	100%
DA3	100%
DA4	70%
DS	60%
SE	70%

Aquí se construye:

Sensor Dataset
      +
Maintenance Dataset
      +
Machine Master
      ↓
Integrated Dataset

11. Fase 3 — Feature Engineering & Baseline
Persona	Carga
DA1	20%
DA2	80%
DA3	80%
DA4	80%
DS	100%
SE	60%

Aquí aparece el primer Risk Score.

No esperaría al modelo sofisticado para mostrar resultados.

Primero:

Baseline → ML → Comparar

12. Fase 4 — Predictive Model
Persona	Carga
DA1	30%
DA2	50%
DA3	60%
DA4	60%
DS	100%
SE	70%

El DS lidera.

Los DAs hacen validación, análisis y contextualización.

SE empieza la integración productiva.

13. Fase 5 — Dashboard & Decision Support
Persona	Carga
DA1	60%
DA2	30%
DA3	30%
DA4	100%
DS	50%
SE	100%

El resultado debería permitir algo como:

Machine Risk Overview
Máquina	Riesgo	Criticidad	Tendencia	Acción
CNC-001	🔴 87%	Alta	↑	Inspeccionar
CNC-002	🟠 62%	Alta	↑	Monitorear
LATHE-003	🟢 12%	Media	→	Ninguna
MILL-004	🔴 91%	Alta	↑	Intervenir

Y al seleccionar una máquina:

Machine: CNC-001

Risk: 87%
Criticality: HIGH

Main signals:
  Vibration       ↑ +32%
  Temperature     ↑ +18%
  Pressure        ↑ +11%

Last maintenance:
  46 days ago

Previous failures:
  3

Recommended action:
  INSPECTION

14. Fase 6 — MVP Production
Persona	Carga
DA1	30%
DA2	20%
DA3	20%
DA4	60%
DS	60%
SE	100%

Aquí el foco cambia de:

"¿Funciona el modelo?"

a:

"¿Puede realmente utilizarlo mantenimiento?"

15. RACI

Yo establecería este RACI inicial:

Actividad	DA1	DA2	DA3	DA4	DS	SE
Business requirements	A/R	C	C	C	C	I
Data inventory	A	R	R	C	C	C
Sensor quality	C	A/R	I	C	C	C
Maintenance analysis	C	I	A/R	C	C	I
Failure definition	A	C	R	I	R	I
Feature engineering	I	R	R	R	A	C
Baseline model	I	C	C	C	A/R	I
ML model	I	C	C	C	A/R	C
Model validation	C	R	R	R	A	I
Dashboard	C	I	C	A/R	C	C
Data pipeline	I	C	C	I	C	A/R
API	I	I	I	C	C	A/R
Deployment	I	I	I	I	C	A/R
Business acceptance	A/R	C	C	C	C	I

A = Accountable
R = Responsible
C = Consulted
I = Informed

16. Un punto crítico: no prometer "cuándo va a fallar" demasiado pronto

Hay una diferencia importante entre:

Anomaly Detection

"Esta máquina se está comportando de forma anormal."

Failure Prediction

"Esta máquina tiene alta probabilidad de fallar en los próximos 14 días."

Remaining Useful Life

"Estimamos que quedan 73 horas de vida útil."

Son problemas de dificultad creciente.

Para el MVP propondría:

Nivel 1

Health Score

🟢 Normal
🟡 Warning
🟠 Elevated Risk
🔴 High Risk

Nivel 2

Probability of failure within X days

Nivel 3

Estimated time to failure / RUL

El Nivel 3 solamente si los datos históricos permiten sostenerlo.

17. Priorización de mantenimiento

Otro punto que considero fundamental:

Risk ≠ Priority

Una máquina puede tener:

Risk = 80%


pero ser una máquina secundaria con reemplazo disponible.

Otra puede tener:

Risk = 55%


pero ser crítica para toda una línea de producción.

Por eso recomiendo separar:

Risk Score

Calculado por el modelo.

Criticality Score

Calculado por negocio.

Maintenance Priority

Combinación:

Maintenance Priority
        =
Risk × Criticality × Business Impact


Por ejemplo:

Machine	Risk	Criticality	Priority
A	90%	0.4	36
B	70%	1.0	70
C	50%	0.9	45

Así el sistema no simplemente dice:

"Esta máquina tiene más probabilidad de fallar."

Sino:

"Esta es la máquina que mantenimiento debería revisar primero."

18. Roadmap que propondría
                 PREDICTIVE MAINTENANCE MVP

       ┌─────────────────────────────────────┐
       │ 1. BUSINESS + DATA DISCOVERY         │
       │ DA1 / DA2 / DA3 / DA4 / DS / SE     │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 2. DATA FOUNDATION                  │
       │ Sensors + Maintenance + Machine     │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 3. FEATURE ENGINEERING              │
       │ DA2 + DA3 + DA4 + DS                │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 4. BASELINE + ML MODEL              │
       │              DS                     │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 5. RISK + CRITICALITY               │
       │ DA1 + DS                            │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 6. DASHBOARD                        │
       │ DA4 + SE                            │
       └──────────────────┬──────────────────┘
                          ↓
       ┌─────────────────────────────────────┐
       │ 7. PRODUCTION MVP                   │
       │             SE + DS                 │
       └─────────────────────────────────────┘

19. Mi recomendación de PM

Hay tres workstreams paralelos, no uno solo:

🟦 Workstream A — Data & Business

DA1 + DA2 + DA3

Construyen la base de conocimiento y datos.

🟩 Workstream B — Data Science

DS + DA2 + DA3

Construyen el sistema de detección/predicción.

🟨 Workstream C — Product & Engineering

DA4 + SE + DA1

Construyen la experiencia que permite tomar decisiones.

Esto evita el típico problema de:

"Esperemos a que Data Science termine el modelo y después hacemos el producto."

En Predictive Maintenance eso suele ser demasiado tarde.

El dashboard, la definición de riesgo, la criticidad y el pipeline deben evolucionar en paralelo con el modelo.

Si quieres, también puedo convertirlo en una versión más ejecutiva/profesional para presentar a stakeholders, con un Project Charter + roadmap de 8–12 semanas + sprints + milestones + Definition of Done.
