"""
signal_utils.py — Noise generation and signal helper functions
Phase 1 — Room-Based ANC
"""

import numpy as np
import soundfile as sf
from scipy import signal


def generate_white_noise(duration_s: float, fs: int, amplitude: float = 0.5) -> np.ndarray:
    """Generate white Gaussian noise of given duration and amplitude."""
    n_samples = int(duration_s * fs)
    noise = amplitude * np.random.randn(n_samples)
    return noise


def generate_pink_noise(duration_s: float, fs: int, amplitude: float = 0.5) -> np.ndarray:
    """Generate pink (1/f) noise using Voss–McCartney algorithm."""
    n_samples = int(duration_s * fs)
    n_rows = 16  # controls pinkness
    array = np.random.randn(n_rows, n_samples // n_rows + 1)
    pink = np.cumsum(array, axis=1)
    pink = pink[-1, :n_samples]
    pink /= np.max(np.abs(pink))
    return amplitude * pink


def generate_sine(frequency: float, duration_s: float, fs: int, amplitude: float = 0.5) -> np.ndarray:
    """Generate single-tone sine wave."""
    t = np.arange(0, duration_s, 1 / fs)
    return amplitude * np.sin(2 * np.pi * frequency * t)


def load_audio(filepath: str, fs: int) -> np.ndarray:
    """Load audio file and resample if necessary."""
    x, file_fs = sf.read(filepath)
    if file_fs != fs:
        x = signal.resample_poly(x, fs, file_fs)
    if x.ndim > 1:
        x = np.mean(x, axis=1)  # mono
    return x


def normalize_signal(x: np.ndarray) -> np.ndarray:
    """Normalize signal to ±1."""
    return x / np.max(np.abs(x))


def compute_snr(original: np.ndarray, residual: np.ndarray) -> float:
    """Compute signal-to-noise ratio improvement."""
    power_orig = np.mean(original**2)
    power_resid = np.mean(residual**2)
    snr_db = 10 * np.log10(power_orig / power_resid)
    return snr_db


def save_audio(filepath: str, data: np.ndarray, fs: int):
    """Save array as .wav file."""
    sf.write(filepath, data, fs)
