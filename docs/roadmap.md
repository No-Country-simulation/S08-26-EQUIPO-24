# Roadmap de 4 semanas

---

## SEMANA 1 — Discovery + Dataset + Data Foundation + EDA inicial + repo + dashboard skeleton

### Día 1
- Problema, usuario, criterio de éxito, alcance.

### Día 2
- Evaluación datasets.

### Día 3
- Selección dataset + profiling.

### Día 4
- Calidad.

### Día 5
- EDA + diseño producto.

### GATE 1
- [x] Dataset seleccionado (Azure PdM)
- [x] Usuario definido (Responsable de mantenimiento)
- [x] Target preliminar (`failure_next_24h`)
- [x] Diccionario (`docs/data_dictionary.md`)
- [x] EDA inicial (`notebooks/03_eda_predictivo.ipynb`)
- [x] GitHub configurado
- [x] Dashboard skeleton

---

## SEMANA 2 — ML + integración inicial

### Día 6
- Preparación ML.

### Día 7
- Baseline / modelo inicial.

### Día 8
- Evaluación.

### Día 9
- Selección y serialización.

### Día 10
- Primera integración.

### GATE 2
- [x] Modelo entrenado (Random Forest, PR-AUC 0.9919)
- [x] Métricas definidas y validadas (4 estrategias de split)
- [x] Artefacto guardado (`models/baseline_model.joblib`, 2.50 MB)
- [x] Dashboard base con integración ML funcional
- [x] Integración básica (modelo + datos reales en dashboard)

---

## SEMANA 3 — Producto

### Día 11
- Ranking de riesgo.

### Día 12
- Criticidad.

### Día 13
- Explicabilidad.

### Día 14
- Detalle de máquina.

### Día 15
- Demo interna.

### GATE 3
- [x] Riesgo (ranking de riesgo con score 0–100)
- [x] Score (probabilidad de falla via `model.predict_proba()`)
- [x] Señales (feature importance en `docs/model.md`)
- [x] Ranking (tabla + bar chart interactivo)
- [x] Criticidad (Alta/Media/Baja según risk_score)
- [x] Prioridad (cola de intervención ordenada por priority_score)

---

## SEMANA 4 — Testing + Deploy + Demo

### Día 16
- Testing.

### Día 17
- Validación de negocio.

### Día 18
- Deploy.

### Día 19
- Documentación + presentación.

### Día 20
- Ensayo final.

### GATE 4
- [x] MVP completo (modelo + dashboard + datos reales)
- [x] Tests pasando (7/7: estructura + prevalencia)
- [x] README actualizado
- [ ] Presentación
- [ ] Demo ejecutada
- [ ] Evidencia criterio éxito