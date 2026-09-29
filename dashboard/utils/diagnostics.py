"""Diagnóstico industrial: mapeo de códigos de error a causas raíz y acciones recomendadas."""

ROOT_CAUSE_MAP = [
    (["VIB", "ROT"], "Root Cause: Resonancia crítica en cojinetes/rodamientos (patrón BPFO)", "#ff5353"),
    (["VOLT"], "Root Cause: Fluctuación transitoria en línea de alimentación eléctrica", "#ffb4ab"),
    (["PRESS"], "Root Cause: Pérdida de presión hidráulica en circuito de retorno", "#a4c9ff"),
    (["TEMP"], "Root Cause: Temperatura elevada en bobinado de inducción estatórica", "#ff8a32"),
]

DEFAULT_ROOT_CAUSE = "Root Cause: Desgaste general de componentes mecánicos"
DEFAULT_ROOT_CAUSE_COLOR = "#9da6bd"

ACTION_RECOMMENDATIONS = {
    "Intervenir": {
        "title": "ACCIÓN REQUERIDA",
        "steps": [
            "Detener la máquina inmediatamente y bloquear energía",
            "Inspeccionar cojinetes y rodamientos por patrón BPFO",
            "Verificar estabilidad de la línea de alimentación eléctrica",
            "Revisar presión hidráulica en circuito de retorno",
            "Programar intervención de mantenimiento correctivo",
        ],
    },
    "Inspeccionar": {
        "title": "REVISIÓN RECOMENDADA",
        "steps": [
            "Programar inspección técnica en las próximas 24-48 h",
            "Monitorear tendencias de vibración y presión",
            "Verificar historial de errores recientes",
            "Validar componentes asociados al riesgo reportado",
        ],
    },
    "Monitorear": {
        "title": "MONITOR REFORZADO",
        "steps": [
            "Continuar con monitoreo preventivo habitual",
            "Observar patrones de vibración y voltaje",
            "Revisar errores recientes en el próximo ciclo",
            "Escalar si el score supera el umbral de alerta",
        ],
    },
    "Ninguna": {
        "title": "OPERACIÓN NORMAL",
        "steps": [
            "Continuar con el monitoreo preventivo habitual",
            "Revisar en el próximo ciclo de mantenimiento programado",
        ],
    },
}


def get_root_cause(error_code: str) -> tuple[str, str]:
    """Map an error code to a (root_cause_text, color) tuple."""
    ec = str(error_code).upper()
    for keywords, cause, color in ROOT_CAUSE_MAP:
        if any(kw in ec for kw in keywords):
            return cause, color
    return DEFAULT_ROOT_CAUSE, DEFAULT_ROOT_CAUSE_COLOR


def get_action_recommendation(priority: str) -> dict:
    """Return action recommendation dict for a given priority level."""
    return ACTION_RECOMMENDATIONS.get(priority, ACTION_RECOMMENDATIONS["Ninguna"])
