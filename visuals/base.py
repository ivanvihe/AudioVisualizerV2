"""Base classes for visuals.

The :class:`BaseVisualizer` encapsulates common controls such as audio
reactivity and smoothing.  Real presets will subclass this and implement the
:meth:`render` method.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

try:  # pragma: no cover - Qt optional
    from PyQt5.QtCore import QObject
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass


@dataclass
class VisualControl:
    """Description of a user facing control."""

    name: str
    default: Any
    minimum: float = 0.0
    maximum: float = 1.0


class BaseVisualizer(QObject):
    """Base class for every visual preset."""

    def __init__(self):
        super().__init__()
        self.controls: Dict[str, VisualControl] = {
            "audio_reactive": VisualControl("Audio Reactive", True, 0, 1),
            "audio_sensitivity": VisualControl("Audio Sensitivity", 1.0, 0, 5),
            "smoothness": VisualControl("Smoothness", 0.5, 0, 1),
        }

    # ------------------------------------------------------------------
    def update_audio(self, bass: float, mid: float, treble: float, level: float) -> None:
        """Called by :class:`AudioAnalyzer` when new data is available.

        The default implementation does nothing but subclasses can store the
        values to drive their animation.
        """

    def render(self, width: int, height: int) -> None:  # pragma: no cover - visual
        """Render the frame.

        Subclasses should perform their drawing here using OpenGL, ModernGL or
        any other rendering backend.  The skeleton has no real rendering code.
        """
