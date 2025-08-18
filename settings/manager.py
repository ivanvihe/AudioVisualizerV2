"""Settings manager handling persistent configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

SETTINGS_FILE = Path("config/settings.json")
MIDI_FILE = Path("config/midi_mappings.json")

# Default configuration files used by the simplified MIDI system.  The real
# project exposes a much richer persistence layer but for the purposes of this
# kata we simply load JSON dictionaries from disk.  ``NOTE_FILE`` maps MIDI note
# numbers to visual preset names while ``CHANNEL_FILE`` associates deck names
# with MIDI channel numbers.
NOTE_FILE = Path("config/preset_notes.json")
CHANNEL_FILE = Path("config/deck_channels.json")


@dataclass
class SettingsManager:
    """Load and save configuration to disk."""

    settings: Dict[str, Any] = field(default_factory=dict)

    def load(self) -> None:
        if SETTINGS_FILE.exists():
            self.settings = json.loads(SETTINGS_FILE.read_text())
        else:
            self.settings = {}

    def save(self) -> None:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps(self.settings, indent=2))


def load_note_mapping(path: Path = NOTE_FILE) -> Dict[int, str]:
    """Return mapping from MIDI notes to visual class names.

    The JSON file uses strings for the note keys so the values are converted
    back to integers for easier processing by the MIDI engine.  When the file
    is missing an empty mapping is returned.
    """

    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {int(k): v for k, v in data.items()}


def load_channel_mapping(path: Path = CHANNEL_FILE) -> Dict[int, str]:
    """Return mapping from MIDI channel numbers to deck identifiers.

    Channels default to ``13`` – ``16`` for decks ``A`` – ``D`` respectively if
    the configuration file is not present.
    """

    if path.exists():
        data = json.loads(path.read_text())
        # The file maps deck names to channel numbers, we invert it to obtain a
        # dictionary keyed by channel for faster lookups.
        return {int(ch): deck for deck, ch in data.items()}
    return {13: "A", 14: "B", 15: "C", 16: "D"}
