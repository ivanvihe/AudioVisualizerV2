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
        # ``control_values`` stores the current user edited value for each
        # control.  By default we simply copy the ``default`` field.
        self.control_values: Dict[str, Any] = {
            name: ctrl.default for name, ctrl in self.controls.items()
        }

        # Smoothed audio levels exposed to subclasses via ``audio_levels``.
        self._audio_level = 0.0
        self._bass = 0.0
        self._mid = 0.0
        self._treble = 0.0

    # ------------------------------------------------------------------
    def set_control(self, name: str, value: Any) -> None:
        """Update the value of a runtime control."""

        if name in self.controls:
            ctrl = self.controls[name]
            # Clamp to the declared range
            val = max(ctrl.minimum, min(ctrl.maximum, value))
            self.control_values[name] = val

    def get_control(self, name: str) -> Any:
        return self.control_values.get(name)

    # ------------------------------------------------------------------
    def update_audio(self, bass: float, mid: float, treble: float, level: float) -> None:
        """Called by :class:`AudioAnalyzer` when new data is available.

        The base implementation applies sensitivity and smoothing so that every
        preset can simply read the values from :meth:`audio_levels`.
        """

        if not self.control_values.get("audio_reactive", True):
            return

        sensitivity = float(self.control_values.get("audio_sensitivity", 1.0))
        smooth = float(self.control_values.get("smoothness", 0.5))

        def smooth_val(old: float, new: float) -> float:
            return smooth * old + (1.0 - smooth) * new * sensitivity

        self._bass = smooth_val(self._bass, bass)
        self._mid = smooth_val(self._mid, mid)
        self._treble = smooth_val(self._treble, treble)
        self._audio_level = smooth_val(self._audio_level, level)

    # ------------------------------------------------------------------
    def audio_levels(self) -> Dict[str, float]:
        """Return the latest smoothed audio levels."""

        return {
            "bass": self._bass,
            "mid": self._mid,
            "treble": self._treble,
            "level": self._audio_level,
        }

    def render(self, width: int, height: int) -> None:  # pragma: no cover - visual
        """Render the frame.

        Subclasses should perform their drawing here using OpenGL, ModernGL or
        any other rendering backend.  The skeleton has no real rendering code.
        """
