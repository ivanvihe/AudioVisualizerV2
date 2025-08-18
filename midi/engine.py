"""Minimal MIDI engine used by AudioVisualizerV2.

The real application interfaces with actual MIDI hardware and offers a rich
mapping system.  This skeleton captures the structure of that system so the
rest of the code base can be built and unit tested without external
dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

try:  # pragma: no cover - Qt is optional
    from PyQt5.QtCore import QObject, pyqtSignal
except Exception:  # pragma: no cover
    class QObject:  # type: ignore
        pass

    def pyqtSignal(*_args, **_kwargs):  # type: ignore
        return None


@dataclass
class MidiMapping:
    """Represents a mapping from a MIDI message to an application action."""

    action: str
    channel: int
    note: int
    min_value: float = 0.0
    max_value: float = 1.0


class MidiEngine(QObject):
    """Dispatch MIDI events to registered callbacks.

    Only a tiny subset of the full project is implemented here: actions can be
    registered with :meth:`map_message` and triggered via
    :meth:`process_message`.
    """

    device_connected = pyqtSignal(str)
    mapped_action_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mappings: List[MidiMapping] = []
        self._callbacks: Dict[str, Callable[[float], None]] = {}

    # ------------------------------------------------------------------
    def map_message(
        self, action: str, channel: int, note: int, callback: Callable[[float], None]
    ) -> None:
        """Register an *action* for the given ``channel`` and ``note``."""

        self.mappings.append(MidiMapping(action, channel, note))
        self._callbacks[action] = callback

    # ------------------------------------------------------------------
    def process_message(self, channel: int, note: int, value: int) -> None:
        """Invoke the callback associated with a MIDI message.

        Parameters are raw MIDI values.  They are normalised to ``0.0`` – ``1.0``
        before being passed to the callback.
        """

        for mapping in self.mappings:
            if mapping.channel == channel and mapping.note == note:
                norm = (value - 0) / 127
                if getattr(self.mapped_action_triggered, "emit", None):
                    self.mapped_action_triggered.emit(mapping.action)
                cb = self._callbacks.get(mapping.action)
                if cb is not None:
                    cb(norm)
                break
