"""Representation of a visual deck.

Each deck owns an instance of a visual preset and manages cross fading and
rendering into an off‑screen buffer.  This file only provides a light‑weight
Python implementation to keep the repository self contained.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from visuals.base import BaseVisualizer
from audio.analyzer import AudioAnalyzer


@dataclass
class Deck:
    """Container that ties a visual to audio analysis."""

    name: str
    analyzer: AudioAnalyzer
    visual: Optional[BaseVisualizer] = None
    opacity: float = 1.0

    def load_visual(self, visual: BaseVisualizer) -> None:
        self.visual = visual

    def render(self, width: int, height: int) -> None:
        if self.visual is not None:
            self.visual.render(width, height)
