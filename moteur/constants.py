# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import sys
from pathlib import Path

# Variables Globales
L, H = 1300, 800
FPS = 120
hitbox_activee = True

def path(p_relatif):
    """
    Petite fonction pour pas péter les plombs avec les chemins 
    quand on compile en .exe (PyInstaller utilise _MEIPASS)
    """
    base = Path(getattr(sys, '_MEIPASS', '.'))
    return base / p_relatif
