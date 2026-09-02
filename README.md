# Predictive Maintenance MVP — Propuesta de Proyecto

> **Código:** S08-26-EQUIPO-24

Con esta definición ya podemos plantear el proyecto como un **MVP de Predictive Maintenance**, y distribuir el trabajo entre 4 Data Analysts, 1 Data Scientist y 1 Software Engineer, sin que todo termine dependiendo del DS.

**Recomendación del PM:** no empezar intentando predecir todas las fallas de todas las máquinas. Primero construir un pipeline completo sobre un subconjunto de máquinas/componentes y demostrar que se puede pasar de:

```
Datos → Riesgo → Explicación → Acción
```

---

## 1. Objetivo del MVP

El MVP debería responder cuatro preguntas:

1. ¿Qué máquinas están mostrando comportamiento anómalo?
2. ¿Qué probabilidad tienen de presentar una falla en un horizonte definido?
3. ¿Qué variables/señales explican ese riesgo?
4. ¿Qué máquinas deberían priorizarse para una intervención?

**Flujo general:**

```
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
```

---

## 2. Distribución propuesta del equipo

| Rol | Responsabilidad principal | Foco |
|---|---|---|
| DA1 | Data & Business Analyst | Entendimiento del negocio, KPIs, criticidad |
| DA2 | Data Quality & Sensor Analyst | Calidad, exploración y comportamiento de sensores |
| DA3 | Maintenance Data Analyst | Historial de mantenimiento y definición de eventos/fallas |
| DA4 | Analytics & Visualization Analyst | Features, análisis exploratorio y dashboard |
| Data Scientist | Predictive Modeling Lead | Anomalías, predicción, evaluación y modelo |
| Software Engineer | Data/ML Platform | Pipeline, APIs, integración y deployment |

La idea central es que los 4 DAs alimenten al DS con datasets, definiciones y análisis preparados, mientras el SE construye la infraestructura necesaria para que el resultado se convierta en producto.

---

## 3. DA1 — Business & Data Analyst

**Misión:** convertir el problema de mantenimiento en requerimientos medibles.

**Tareas**
- Identificar stakeholders: mantenimiento, producción, operaciones, ingeniería.
- Definir qué significa una falla.
- Definir qué significa: máquina crítica, máquina bajo observación, máquina de alto riesgo, intervención prioritaria.
- Identificar KPIs de negocio: downtime, costo de reparación, número de fallas, MTBF, MTTR, costo de mantenimiento.
- Definir horizonte de predicción (ej. riesgo de falla en próximos 7/14/30 días).
- Definir criterios de éxito del MVP.
- Construir matriz de criticidad de máquinas.
- Traducir el output del modelo a una lógica de priorización para mantenimiento.

**Entregables**
- Business Requirements Document
- Data Dictionary de negocio
- Definición de falla/evento
- Matriz de criticidad
- KPIs
- Reglas de priorización
- Acceptance Criteria

**Dependencia:** DA1 debería trabajar desde el día 1 con el responsable de mantenimiento.

---

## 4. DA2 — Data Quality & Sensor Analyst

**Misión:** entender si los datos de sensores realmente pueden utilizarse para detectar deterioro.

**Tareas**
- Inventario de sensores.
- Identificar: frecuencia de medición, unidades, rangos, missing values, outliers, duplicados, gaps temporales.
- Analizar calidad por máquina.
- Analizar distribución de: temperatura, vibración, presión, velocidad, consumo, ciclos.
- Detectar sensores defectuosos.
- Analizar cambios de comportamiento.
- Identificar patrones previos a eventos de mantenimiento.
- Investigar correlaciones entre variables.
- Generar baseline de comportamiento normal.

**Entregables**
- Sensor Data Quality Report
- Dataset limpio de sensores
- Data profiling
- Baseline de comportamiento
- Lista de variables candidatas
- Reglas de calidad

**Especial atención:** DA2 debería trabajar estrechamente con el Data Scientist, porque aquí se define qué señales pueden convertirse en features.

---

## 5. DA3 — Maintenance Data Analyst

> Este rol es especialmente importante.

**Misión:** transformar el historial de mantenimiento en labels/eventos utilizables por Machine Learning.

Hay que resolver algo fundamental: **¿qué significa exactamente que una máquina "falló"?**

No necesariamente `maintenance_record = failure`. Puede haber: mantenimiento preventivo, inspección, lubricación, cambio de pieza, reparación, falla, emergencia, ajuste, calibración.

**Tareas**
- Analizar histórico de mantenimiento.
- Clasificar tipos de intervención.
- Identificar verdaderas fallas.
- Identificar componentes afectados.
- Construir timeline por máquina.

**Ejemplo — Machine A:**

```
01/01 → Normal
05/01 → Maintenance
12/01 → Increasing vibration
15/01 → Alarm
17/01 → Failure
18/01 → Bearing replacement
```

- Relacionar sensores, alarmas, mantenimiento, fallas y componentes.
- Construir dataset de eventos.
- Analizar frecuencia de fallas.
- Analizar tiempo entre fallas.
- Identificar componentes con mayor recurrencia.

**Entregables**
- Maintenance Event Dataset
- Failure Label Definition
- Failure Taxonomy
- Machine Failure Timeline
- Component Failure Analysis
- Dataset para entrenamiento

> Este trabajo es probablemente uno de los mayores cuellos de botella del proyecto, por lo que se asignaría bastante capacidad de DA3 inicialmente.

---

## 6. DA4 — Analytics & Visualization Analyst

**Misión:** convertir los datos preparados en insights y visualizaciones accionables.

**Tareas**
- EDA integrado.
- Crear vistas por máquina.
- Crear tendencias de sensores.
- Analizar comportamiento pre-falla.
- Crear variables agregadas: media móvil, desviación estándar, máximo/mínimo, tendencia, tasa de cambio, rolling statistics.
- Diseñar mockups del dashboard.
- Definir UX para mantenimiento.
- Construir dashboard MVP.
- Visualizar: Risk Score, criticidad, tendencia, últimas alarmas, mantenimiento, fallas, señales relevantes.

**Entregables**
- EDA integrado
- Feature candidates
- Dashboard prototype
- Risk visualization
- Machine detail view
- Maintenance prioritization view

> DA4 debería comenzar el diseño del dashboard antes de tener el modelo terminado, no después.

---

## 7. Data Scientist

**Misión:** desarrollar el motor predictivo. El DS no debería encargarse de limpiar todo el dataset ni de construir el dashboard; su tiempo debe concentrarse en el problema de ML.

### Fase 1 — Baseline

Antes de un modelo complejo: baseline histórico, reglas simples, threshold de sensores, anomaly detection básico.

```
IF vibration > threshold
AND temperature trend increasing
THEN elevated risk
```

Esto permite comparar posteriormente contra ML.

### Fase 2 — Feature Engineering

Con apoyo de DA2 y DA3: rolling mean, rolling std, trend, rate of change, sensor interactions, time since maintenance, operating hours, cycles, previous failures, component age.

### Fase 3 — Modelos

Dependiendo de la cantidad/calidad de datos:

- **Supervised:** Logistic Regression, Random Forest, XGBoost / LightGBM
- **Unsupervised / Anomaly Detection:** Isolation Forest, clustering, autoencoders (si están justificados)
- **Survival / Remaining Useful Life:** Survival Analysis, Cox models, RUL models — *evaluar posteriormente, no como requisito del MVP*

### Fase 4 — Evaluación

Muy importante: **no evaluar solamente accuracy.** Medir: Precision, Recall, F1, PR-AUC, False Negatives, False Positives, Lead Time.

Pregunta clave: ¿cuánto tiempo antes de la falla se consigue detectar el deterioro?

### Fase 5 — Explainability

El mantenimiento debe poder entender "¿por qué esta máquina tiene riesgo alto?". El DS debería entregar: principales features, contribution de variables, tendencias relevantes, explicación del score.

**Entregables**
- Baseline
- Feature dataset
- Anomaly detection
- Predictive model
- Model evaluation
- Risk score
- Explainability
- Model artifact
- Inference specification

---

## 8. Software Engineer

**Misión:** convertir el análisis/modelo en un sistema ejecutable y mantenible.

**Data Ingestion**
```
Sensor data → Raw data → Processed data → Feature data
```

**Data Pipeline:** automatización de ingestion, transformación, validación, feature generation, scoring.

**ML Integration**
```
New sensor data → Pipeline → Features → ML model → Risk Score
```

**Backend:** API para consultar machine, current status, risk score, alerts, historical trends, explanations.

**Frontend Integration** (si el MVP requiere aplicación web)
```
Dashboard → API → Prediction service → Data / ML layer
```

**Deployment:** environment, CI/CD, logging, monitoring, model versioning, error handling.

**Entregables**
- Data pipeline
- Feature pipeline
- Model serving
- API
- Backend
- Deployment
- Monitoring básico
- Integración con dashboard

---

## 9. Fases del proyecto

Se proponen **6 fases**.

### Fase 1 — Discovery & Data Assessment

*Objetivo: saber si hay datos suficientes para hacer el proyecto.*

| Persona | Carga |
|---|---|
| DA1 | 80% |
| DA2 | 100% |
| DA3 | 100% |
| DA4 | 50% |
| DS | 30% |
| SE | 20% |

DA1 define negocio · DA2 analiza sensores · DA3 analiza mantenimiento · DS evalúa factibilidad ML · SE entiende fuentes e infraestructura.

### Fase 2 — Data Foundation

*Objetivo: construir datasets confiables.*

| Persona | Carga |
|---|---|
| DA1 | 40% |
| DA2 | 100% |
| DA3 | 100% |
| DA4 | 70% |
| DS | 60% |
| SE | 70% |

```
Sensor Dataset + Maintenance Dataset + Machine Master → Integrated Dataset
```

### Fase 3 — Feature Engineering & Baseline

| Persona | Carga |
|---|---|
| DA1 | 20% |
| DA2 | 80% |
| DA3 | 80% |
| DA4 | 80% |
| DS | 100% |
| SE | 60% |

Aquí aparece el primer Risk Score. No se espera al modelo sofisticado para mostrar resultados: **Baseline → ML → Comparar**.

### Fase 4 — Predictive Model

| Persona | Carga |
|---|---|
| DA1 | 30% |
| DA2 | 50% |
| DA3 | 60% |
| DA4 | 60% |
| DS | 100% |
| SE | 70% |

El DS lidera. Los DAs hacen validación, análisis y contextualización. SE empieza la integración productiva.

### Fase 5 — Dashboard & Decision Support

| Persona | Carga |
|---|---|
| DA1 | 60% |
| DA2 | 30% |
| DA3 | 30% |
| DA4 | 100% |
| DS | 50% |
| SE | 100% |

**Machine Risk Overview (ejemplo):**

| Máquina | Riesgo | Criticidad | Tendencia | Acción |
|---|---|---|---|---|
| CNC-001 | 🔴 87% | Alta | ↑ | Inspeccionar |
| CNC-002 | 🟠 62% | Alta | ↑ | Monitorear |
| LATHE-003 | 🟢 12% | Media | → | Ninguna |
| MILL-004 | 🔴 91% | Alta | ↑ | Intervenir |

**Detalle al seleccionar una máquina (ejemplo):**

```
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
```

### Fase 6 — MVP Production

| Persona | Carga |
|---|---|
| DA1 | 30% |
| DA2 | 20% |
| DA3 | 20% |
| DA4 | 60% |
| DS | 60% |
| SE | 100% |

El foco cambia de *"¿funciona el modelo?"* a *"¿puede realmente utilizarlo mantenimiento?"*.

---

## 10. RACI

| Actividad | DA1 | DA2 | DA3 | DA4 | DS | SE |
|---|---|---|---|---|---|---|
| Business requirements | A/R | C | C | C | C | I |
| Data inventory | A | R | R | C | C | C |
| Sensor quality | C | A/R | I | C | C | C |
| Maintenance analysis | C | I | A/R | C | C | I |
| Failure definition | A | C | R | I | R | I |
| Feature engineering | I | R | R | R | A | C |
| Baseline model | I | C | C | C | A/R | I |
| ML model | I | C | C | C | A/R | C |
| Model validation | C | R | R | R | A | I |
| Dashboard | C | I | C | A/R | C | C |
| Data pipeline | I | C | C | I | C | A/R |
| API | I | I | I | C | C | A/R |
| Deployment | I | I | I | I | C | A/R |
| Business acceptance | A/R | C | C | C | C | I |

*A = Accountable · R = Responsible · C = Consulted · I = Informed*

---

## 11. Punto crítico: no prometer "cuándo va a fallar" demasiado pronto

Hay una diferencia importante entre tres niveles de dificultad creciente:

| Nivel | Concepto | Ejemplo de salida |
|---|---|---|
| Anomaly Detection | Comportamiento anormal | "Esta máquina se está comportando de forma anormal." |
| Failure Prediction | Probabilidad de falla | "Esta máquina tiene alta probabilidad de fallar en los próximos 14 días." |
| Remaining Useful Life | Vida útil restante | "Estimamos que quedan 73 horas de vida útil." |

**Propuesta para el MVP:**

- **Nivel 1 — Health Score:** 🟢 Normal · 🟡 Warning · 🟠 Elevated Risk · 🔴 High Risk
- **Nivel 2 — Probability of failure within X days**
- **Nivel 3 — Estimated time to failure / RUL** — solo si los datos históricos permiten sostenerlo

---

## 12. Priorización de mantenimiento

**Risk ≠ Priority**

- Una máquina puede tener Risk = 80% pero ser secundaria con reemplazo disponible.
- Otra puede tener Risk = 55% pero ser crítica para toda una línea de producción.

Por eso se recomienda separar:

- **Risk Score** — calculado por el modelo.
- **Criticality Score** — calculado por negocio.
- **Maintenance Priority** — combinación:

```
Maintenance Priority = Risk × Criticality × Business Impact
```

| Machine | Risk | Criticality | Priority |
|---|---|---|---|
| A | 90% | 0.4 | 36 |
| B | 70% | 1.0 | 70 |
| C | 50% | 0.9 | 45 |

Así el sistema no dice solamente *"esta máquina tiene más probabilidad de fallar"*, sino *"esta es la máquina que mantenimiento debería revisar primero"*.

---

## 13. Roadmap propuesto

```
                 PREDICTIVE MAINTENANCE MVP

       ┌─────────────────────────────────────┐
       │ 1. BUSINESS + DATA DISCOVERY         │
       │ DA1 / DA2 / DA3 / DA4 / DS / SE      │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 2. DATA FOUNDATION                   │
       │ Sensors + Maintenance + Machine      │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 3. FEATURE ENGINEERING               │
       │ DA2 + DA3 + DA4 + DS                 │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 4. BASELINE + ML MODEL               │
       │              DS                      │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 5. RISK + CRITICALITY                │
       │ DA1 + DS                             │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 6. DASHBOARD                         │
       │ DA4 + SE                             │
       └──────────────────┬──────────────────┘
                           ↓
       ┌─────────────────────────────────────┐
       │ 7. PRODUCTION MVP                    │
       │             SE + DS                  │
       └─────────────────────────────────────┘
```

---

## 14. Recomendación final del PM

Hay **tres workstreams paralelos**, no uno solo:

- 🟦 **Workstream A — Data & Business:** DA1 + DA2 + DA3 → construyen la base de conocimiento y datos.
- 🟩 **Workstream B — Data Science:** DS + DA2 + DA3 → construyen el sistema de detección/predicción.
- 🟨 **Workstream C — Product & Engineering:** DA4 + SE + DA1 → construyen la experiencia que permite tomar decisiones.

Esto evita el típico problema de *"esperemos a que Data Science termine el modelo y después hacemos el producto"*. En Predictive Maintenance eso suele ser demasiado tarde: el dashboard, la definición de riesgo, la criticidad y el pipeline deben evolucionar en paralelo con el modelo.

> Siguiente paso posible: convertir esta propuesta en una versión más ejecutiva/profesional para presentar a stakeholders, con un Project Charter + roadmap de 8–12 semanas + sprints + milestones + Definition of Done.
