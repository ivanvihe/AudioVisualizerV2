"""Settings manager handling persistent configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

SETTINGS_FILE = Path("config/settings.json")
MIDI_FILE = Path("config/midi_mappings.json")


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
