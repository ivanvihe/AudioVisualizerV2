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
    fade_ms: int = 300

    # Internal state used during visual transitions
    _next_visual: Optional[BaseVisualizer] = field(default=None, init=False, repr=False)
    _fade_progress: float = field(default=1.0, init=False, repr=False)
    _transition_duration: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        # Forward FFT data from the analyser to the visual so presets can react
        # to audio without having to manage the connection themselves.
        if hasattr(self.analyzer, "fft_data_ready") and getattr(
            self.analyzer.fft_data_ready, "connect", None
        ):
            self.analyzer.fft_data_ready.connect(self._on_fft)  # pragma: no cover

    # ------------------------------------------------------------------
    def _on_fft(self, spectrum):  # pragma: no cover - requires Qt loop
        if self.visual is None:
            return
        bass = self.analyzer.get_bass(spectrum)
        mid = self.analyzer.get_mid(spectrum)
        treble = self.analyzer.get_treble(spectrum)
        level = self.analyzer.peak_level()
        self.visual.update_audio(bass, mid, treble, level)

    # ------------------------------------------------------------------
    def set_opacity(self, value: float) -> None:
        """Set deck transparency in the range ``0`` – ``1``."""

        self.opacity = max(0.0, min(1.0, value))

    def load_visual(self, visual: BaseVisualizer, fade_ms: Optional[int] = None) -> None:
        """Load *visual* into the deck with optional cross‑fade."""

        fade = fade_ms if fade_ms is not None else self.fade_ms
        if self.visual is None or fade <= 0:
            self.visual = visual
            self._next_visual = None
            self._fade_progress = 1.0
        else:
            self._next_visual = visual
            self._fade_progress = 0.0
            self._transition_duration = fade

    def render(self, width: int, height: int) -> None:
        # Update transition progress when a new visual is queued.  This is a
        # very small time based approximation suitable for the non realtime
        # environment of the kata.  In the actual application the progress would
        # be tied to a clock and used to blend two frame buffers.
        if self._next_visual is not None and self._transition_duration > 0:
            step = 1.0 / float(self._transition_duration)
            self._fade_progress = min(1.0, self._fade_progress + step)
            if self._fade_progress >= 1.0:
                self.visual = self._next_visual
                self._next_visual = None

        if self.visual is not None:
            # ``opacity`` would multiply the rendered image in a real engine.
            self.visual.render(width, height)
