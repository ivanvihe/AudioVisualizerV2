"""Utilities for managing custom thumbnails for presets."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

THUMBNAIL_FILE = Path("config/custom_thumbnails.json")


@dataclass
class ThumbnailInfo:
    visual_name: str
    path: str


def load_thumbnails() -> Dict[str, ThumbnailInfo]:
    """Return mapping of visual name to :class:`ThumbnailInfo`."""

    if not THUMBNAIL_FILE.exists():
        return {}
    data = json.loads(THUMBNAIL_FILE.read_text())
    return {k: ThumbnailInfo(k, v) for k, v in data.items()}


def save_thumbnails(mapping: Dict[str, ThumbnailInfo]) -> None:
    THUMBNAIL_FILE.parent.mkdir(parents=True, exist_ok=True)
    json.dump({k: v.path for k, v in mapping.items()}, THUMBNAIL_FILE.open("w"), indent=2)
