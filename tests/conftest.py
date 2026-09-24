"""Configuración de pytest: hace importable el paquete `dashboard`."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# app.py importa `utils.*` y `components.*` como paquetes de primer nivel.
sys.path.insert(0, os.path.join(ROOT, "dashboard"))
