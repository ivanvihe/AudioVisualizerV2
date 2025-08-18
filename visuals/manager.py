"""Utilities for loading and managing visual presets."""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Dict, Type

from .base import BaseVisualizer


@dataclass
class VisualInfo:
    """Metadata about a visual preset."""

    name: str
    cls: Type[BaseVisualizer]


class VisualizerManager:
    """Discover and instantiate available visuals."""

    def __init__(self):
        self.visuals: Dict[str, VisualInfo] = {}

    def scan(self, package: str = "visuals.presets") -> None:
        """Scan *package* for subclasses of :class:`BaseVisualizer`.

        In the full application this supports hot reloading.  Here we simply
        import every module below ``visuals.presets`` once.
        """

        self.visuals.clear()
        try:
            pkg = importlib.import_module(package)
        except Exception:  # pragma: no cover - package missing
            return

        for mod_info in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
            module = importlib.import_module(mod_info.name)
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseVisualizer):
                    self.visuals[attr] = VisualInfo(name=attr, cls=obj)

    def create(self, name: str) -> BaseVisualizer:
        """Instantiate a visual by its class name."""

        info = self.visuals[name]
        return info.cls()
