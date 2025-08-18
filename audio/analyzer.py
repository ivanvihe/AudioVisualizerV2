"""Audio analysis core for AudioVisualizerV2.

This module provides :class:`AudioAnalyzer`, a Qt aware object capable of
producing demo audio or capturing real hardware input.  It computes a FFT
using a Hanning window and emits convenient signals with the spectral data
and smoothed global levels.

The real project would rely on :mod:`pyaudio` for realtime capture.  In this
skeleton implementation the analyser only generates a sine wave so that the
rest of the application can be tested without external dependencies.
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass

try:  # pragma: no cover - Qt is optional in this skeleton
    from PyQt5.QtCore import QObject, pyqtSignal, QTimer
except Exception:  # pragma: no cover
    # Minimal stand‑ins so the module can be compiled without Qt installed.
    class QObject:  # type: ignore
        pass

    def pyqtSignal(*_args, **_kwargs):  # type: ignore
        return None

    class QTimer:  # type: ignore
        def __init__(self):
            self.interval = 0

        def start(self, interval):
            self.interval = interval

        def stop(self):
            self.interval = 0


@dataclass
class AudioSettings:
    """Configuration used by :class:`AudioAnalyzer`.

    Attributes
    ----------
    sample_rate:
        Sampling frequency used for the generated signal.
    fft_size:
        Number of samples used for the FFT calculation.
    smoothing_factor:
        Exponential smoothing used when emitting the global audio level.
    """

    sample_rate: int = 44100
    fft_size: int = 1024
    smoothing_factor: float = 0.5


class AudioAnalyzer(QObject):
    """Produce FFT and level information from an audio source.

    The class exposes three Qt signals:

    ``fft_data_ready``
        Emitted with the FFT magnitude array.
    ``audio_data_ready``
        Raw audio samples (mostly for visualisations requiring waveform).
    ``level_changed``
        Global level in the range ``0.0`` – ``1.0``.
    """

    fft_data_ready = pyqtSignal(np.ndarray)
    audio_data_ready = pyqtSignal(np.ndarray)
    level_changed = pyqtSignal(float)

    def __init__(self, settings: AudioSettings | None = None, demo: bool = True):
        super().__init__()
        self.settings = settings or AudioSettings()
        self.demo = demo
        self._phase = 0.0
        self._level = 0.0
        self.timer = QTimer()
        # Update roughly at 60 Hz for smooth animations.
        self.timer_interval_ms = int(1000 / 60)

    # ------------------------------------------------------------------
    # Public API
    def start(self) -> None:
        """Begin emitting demo audio.

        In the full application this method would also open the input device
        when *demo* is ``False``.  Here we simply start an internal timer that
        periodically generates a sine wave chunk and performs the FFT.
        """

        self.timer.start(self.timer_interval_ms)
        # In real code the timer would call ``self._process`` periodically.

    def stop(self) -> None:
        """Stop audio processing."""

        self.timer.stop()

    # ------------------------------------------------------------------
    # Demo signal generation and FFT processing
    def _process(self) -> None:  # pragma: no cover - requires timer
        t = np.arange(self.settings.fft_size)
        freq = 440.0  # A4 reference tone
        phase_increment = 2 * np.pi * freq / self.settings.sample_rate
        self._phase += phase_increment * self.settings.fft_size
        chunk = np.sin(phase_increment * t + self._phase)

        self.audio_data_ready.emit(chunk)
        window = np.hanning(len(chunk))
        spectrum = np.fft.rfft(chunk * window)
        magnitude = np.abs(spectrum)
        self.fft_data_ready.emit(magnitude)

        peak = float(magnitude.max())
        self._level = (
            self.settings.smoothing_factor * self._level
            + (1 - self.settings.smoothing_factor) * peak
        )
        self.level_changed.emit(self._level)

    # ------------------------------------------------------------------
    # Convenience helpers used by visuals
    def get_band(self, spectrum: np.ndarray, start: int, end: int) -> float:
        """Return the average magnitude for a frequency band."""

        if start >= end:
            return 0.0
        return float(np.mean(spectrum[start:end]))

    def get_bass(self, spectrum: np.ndarray) -> float:
        return self.get_band(spectrum, 0, 10)

    def get_mid(self, spectrum: np.ndarray) -> float:
        return self.get_band(spectrum, 10, 40)

    def get_treble(self, spectrum: np.ndarray) -> float:
        return self.get_band(spectrum, 40, len(spectrum))

    def peak_level(self) -> float:
        """Return the last smoothed peak level."""

        return self._level
