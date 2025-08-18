"""Placeholder visual preset."""
from __future__ import annotations

from visuals.base import BaseVisualizer, VisualControl

class OneshotBoomExplosion(BaseVisualizer):
    """Auto generated visual stub."""
    def __init__(self):
        super().__init__()
        self.controls.update({
            "intensity": VisualControl("Intensity", 0.5, 0, 1),
            "size": VisualControl("Size", 0.5, 0, 1),
            "color_mode": VisualControl("Color Mode", 0.5, 0, 1),
        })

    def render(self, width: int, height: int) -> None:  # pragma: no cover - visual
        pass