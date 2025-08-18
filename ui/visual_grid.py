"""Grid view listing all available visuals.

The real project displays thumbnails in a QWidget grid.  This stub merely
stores the names and exposes a ``visual_selected`` signal so tests can trigger
loading of presets without a graphical environment.
"""
from __future__ import annotations

try:  # pragma: no cover - Qt optional
    from PyQt5.QtCore import QObject, pyqtSignal
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass

    def pyqtSignal(*_args, **_kwargs):  # type: ignore
        return None


class VisualGridWindow(QObject):
    """Hold the list of visuals and emit a signal when one is chosen."""

    visual_selected = pyqtSignal(str)

    def __init__(self, visuals):
        super().__init__()
        self.visuals = list(visuals)

    def select_visual(self, name: str) -> None:
        """Trigger selection of a visual by *name*."""

        if name in self.visuals and getattr(self.visual_selected, "emit", None):
            self.visual_selected.emit(name)
