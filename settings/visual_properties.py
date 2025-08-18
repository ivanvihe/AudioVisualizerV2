"""Utilities to store per‑visual parameter values."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

PROPERTIES_FILE = Path("config/visual_properties.json")


def load_properties() -> Dict[str, Dict[str, Any]]:
    if not PROPERTIES_FILE.exists():
        return {}
    return json.loads(PROPERTIES_FILE.read_text())


def save_properties(props: Dict[str, Dict[str, Any]]) -> None:
    PROPERTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROPERTIES_FILE.write_text(json.dumps(props, indent=2))
