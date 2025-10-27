"""
signal_utils.py — Noise generation and signal helper functions
Phase 1 — Room-Based ANC
"""

import numpy as np
import soundfile as sf
from scipy import signal

def generate_white_noise(duration_s : float, fs : int, amplitude : float = 0.5) -> np.ndarray:
    """
    Generate white noise signal.

    Parameters:
    duration_s (float): Duration of the noise in seconds.
    fs (int): Sampling frequency in Hz.
    amplitude (float): Amplitude of the noise signal.

    Returns:
    np.ndarray: Generated white noise signal.
    """
    num_samples = int(duration_s * fs)
    noise = amplitude * np.random.normal(0, 1, num_samples)
    return noise

def generate_pink_noise(duration_s : float, fs : int, amplitude : float = 0.5) -> np.ndarray:
    """
    Generate pink noise signal using Voss-McCartney algorithm.

    Parameters:
    duration_s (float): Duration of the noise in seconds.
    fs (int): Sampling frequency in Hz.
    amplitude (float): Amplitude of the noise signal.

    Returns:
    np.ndarray: Generated pink noise signal.
    """
    num_samples = int(duration_s * fs)
    num_rows = 16
    array = np.zeros((num_rows, num_samples))
    array[0, :] = np.random.normal(0, 1, num_samples)
    
    for i in range(1, num_rows):
        step = 2 ** i
        for j in range(0, num_samples, step):
            array[i, j:j+step] = np.random.normal(0, 1)
    
    pink_noise = np.sum(array, axis=0)
    pink_noise = amplitude * pink_noise / np.max(np.abs(pink_noise))
    
    return pink_noise

def generate_sine(frequency_hz : float, duration_s : float, fs : int, amplitude : float = 0.5) -> np.ndarray:
    """
    Generate a sine wave signal.

    Parameters:
    frequency_hz (float): Frequency of the sine wave in Hz.
    duration_s (float): Duration of the sine wave in seconds.
    fs (int): Sampling frequency in Hz.
    amplitude (float): Amplitude of the sine wave.

    Returns:
    np.ndarray: Generated sine wave signal.
    """
    t = np.linspace(0, duration_s, int(fs * duration_s), endpoint=False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency_hz * t)
    return sine_wave

def load_audio(file_path : str, target_fs : int = None) -> (np.ndarray, int):
    """
    Load an audio file and optionally resample it to a target sampling frequency.

    Parameters:
    file_path (str): Path to the audio file.
    target_fs (int): Target sampling frequency in Hz. If None, no resampling is done.

    Returns:
    tuple: A tuple containing the audio signal (np.ndarray) and its sampling frequency (int).
    """
    signal, fs = sf.read(file_path)
    
    if target_fs is not None and fs != target_fs:
        number_of_samples = round(len(signal) * float(target_fs) / fs)
        signal = signal.resample(signal, number_of_samples)
        fs = target_fs
    
    return signal, fs

def normalize_signal(signal : np.ndarray) -> np.ndarray:
    """
    Normalize a signal to the range [-1, 1].

    Parameters:
    signal (np.ndarray): Input signal.

    Returns:
    np.ndarray: Normalized signal.
    """
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal
    return signal / max_val

def compute_snr(clean_signal : np.ndarray, noise_signal : np.ndarray) -> float:
    """
    Compute the Signal-to-Noise Ratio (SNR) in decibels.

    Parameters:
    clean_signal (np.ndarray): The clean signal.
    noise_signal (np.ndarray): The noise signal.

    Returns:
    float: SNR value in decibels.
    """
    power_clean = np.mean(clean_signal ** 2)
    power_noise = np.mean(noise_signal ** 2)
    
    if power_noise == 0:
        return float('inf')
    
    snr = 10 * np.log10(power_clean / power_noise)
    return snr

def save_audio(file_path : str, signal : np.ndarray, fs : int):
    """
    Save an audio signal to a file.

    Parameters:
    file_path (str): Path to save the audio file.
    signal (np.ndarray): Audio signal to save.
    fs (int): Sampling frequency in Hz.
    """
    sf.write(file_path, signal, fs) 