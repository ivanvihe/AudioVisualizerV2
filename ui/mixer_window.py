"""Mixer window that blends two decks."""
from __future__ import annotations

try:  # pragma: no cover - Qt optional
    from PyQt5.QtCore import QObject, pyqtSignal
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass

    def pyqtSignal(*_args, **_kwargs):  # type: ignore
        return None

from deck import Deck


class MixerWindow(QObject):
    """Very small stub of the real time mixer."""

    crossfader_changed = pyqtSignal(float)

    def __init__(self, deck_a: Deck, deck_b: Deck):
        super().__init__()
        self.deck_a = deck_a
        self.deck_b = deck_b
        self.mix_value = 0.5  # 0 – deck A, 1 – deck B
        self.global_brightness = 1.0

    # ------------------------------------------------------------------
    def set_mix(self, value: float) -> None:
        """Set crossfader value in the range ``0`` – ``1``."""

        self.mix_value = max(0.0, min(1.0, value))
        self.crossfader_changed.emit(self.mix_value)

    def render(self, width: int, height: int) -> None:
        """Render both decks and blend them.

        This method only forwards the call to the decks.  Real blending would be
        performed with an OpenGL shader.
        """

        self.deck_a.render(width, height)
        self.deck_b.render(width, height)
