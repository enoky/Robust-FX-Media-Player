from __future__ import annotations

import math
import os
import shutil
from typing import Optional

from PySide6 import QtGui


def have_exe(name: str) -> bool:
    return shutil.which(name) is not None


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def semitones_to_factor(semitones: float) -> float:
    return float(2.0 ** (semitones / 12.0))


def format_time(seconds: float) -> str:
    if not math.isfinite(seconds) or seconds < 0:
        seconds = 0.0
    total = int(seconds + 0.5)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


def safe_float(x: str, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def env_flag(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def adjust_color(color: str, *, lighter: Optional[int] = None, darker: Optional[int] = None) -> str:
    qt_color = QtGui.QColor(color)
    if lighter is not None:
        qt_color = qt_color.lighter(lighter)
    if darker is not None:
        qt_color = qt_color.darker(darker)
    return qt_color.name()
