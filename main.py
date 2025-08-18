"""Entry point assembling the main application objects."""
from __future__ import annotations

try:  # pragma: no cover - Qt optional
    from PyQt5.QtCore import QObject
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass

from audio.analyzer import AudioAnalyzer
from deck import Deck
from midi.engine import MidiEngine
from settings.manager import SettingsManager
from ui.control_panel import ControlPanelWindow
from ui.mixer_window import MixerWindow
from visuals.manager import VisualizerManager


class MainApplication(QObject):
    """Boot‑strap all subsystems and expose a minimal API."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.settings.load()
        self.audio = AudioAnalyzer()
        self.midi = MidiEngine()
        self.visuals = VisualizerManager()
        self.visuals.scan()

        self.deck_a = Deck("A", analyzer=self.audio)
        self.deck_b = Deck("B", analyzer=self.audio)
        self.mixer = MixerWindow(self.deck_a, self.deck_b)
        self.control_panel = ControlPanelWindow(self.deck_a, self.deck_b)

    def start(self):  # pragma: no cover - requires Qt loop
        self.audio.start()
