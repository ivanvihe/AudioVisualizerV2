"""Simplified control panel window.

The real project exposes a multi‑tabbed interface with live controls and MIDI
configuration.  Here we simply keep track of parameters for the active deck.
"""
from __future__ import annotations

from typing import Dict, Any

try:  # pragma: no cover - Qt optional
    from PyQt5.QtCore import QObject
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass

from deck import Deck


class ControlPanelWindow(QObject):
    """Store parameters for the active deck."""

    def __init__(self, deck_a: Deck, deck_b: Deck):
        super().__init__()
        self.deck_a = deck_a
        self.deck_b = deck_b
        self.active_deck = deck_a
        self.parameters: Dict[str, Any] = {}

    def set_active_deck(self, deck: Deck) -> None:
        self.active_deck = deck

    def update_parameter(self, name: str, value: Any) -> None:
        self.parameters[name] = value
        if name == "opacity":
            # Special case: deck level transparency control
            self.active_deck.set_opacity(float(value))
            return

        visual = self.active_deck.visual
        if visual and name in visual.controls:
            # Forward parameter changes directly to the visual preset so that
            # audio reactivity controls such as sensitivity or smoothness take
            # effect immediately.
            visual.set_control(name, value)
