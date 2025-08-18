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
from settings.manager import (
    SettingsManager,
    load_note_mapping,
    load_channel_mapping,
)
from ui.control_panel import ControlPanelWindow
from ui.mixer_window import MixerWindow
from ui.visual_grid import VisualGridWindow
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

        # Load MIDI note → visual and channel → deck mappings.
        self.note_mapping = load_note_mapping()
        self.channel_mapping = load_channel_mapping()

        # Create four decks A–D.
        self.decks = {
            name: Deck(name, analyzer=self.audio) for name in ["A", "B", "C", "D"]
        }
        self.deck_a = self.decks["A"]
        self.deck_b = self.decks["B"]
        self.deck_c = self.decks["C"]
        self.deck_d = self.decks["D"]

        # Simple mixer and control panel still operate on the first two decks.
        self.mixer = MixerWindow(self.deck_a, self.deck_b)
        self.control_panel = ControlPanelWindow(self.deck_a, self.deck_b)

        # Build MIDI mappings so that each note loads the preset on the deck
        # associated with the incoming channel.
        for note, visual_name in self.note_mapping.items():
            for channel, deck_name in self.channel_mapping.items():
                deck = self.decks[deck_name]

                def make_cb(deck=deck, visual_name=visual_name):
                    def cb(value: float) -> None:
                        if value > 0.0:
                            deck.load_visual(self.visuals.create(visual_name))

                    return cb

                action = f"load_{visual_name}_{deck_name}"
                self.midi.map_message(action, channel, note, make_cb())

        # Main grid listing all available visuals.  Selecting a visual loads it
        # into deck A by default.
        self.grid = VisualGridWindow(self.visuals.visuals.keys())
        if getattr(self.grid.visual_selected, "connect", None):
            self.grid.visual_selected.connect(self._on_visual_selected)  # pragma: no cover

    # ------------------------------------------------------------------
    def _on_visual_selected(self, name: str) -> None:  # pragma: no cover - UI hook
        self.decks["A"].load_visual(self.visuals.create(name))

    def start(self):  # pragma: no cover - requires Qt loop
        self.audio.start()
