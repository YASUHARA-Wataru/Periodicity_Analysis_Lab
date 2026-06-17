from dataclasses import dataclass
import numpy as np

@dataclass
class FrameResult:

    fft_score: np.ndarray
    ac_score: np.ndarray
    yin_score: np.ndarray
    bedcmm_score: np.ndarray

@dataclass
class AnalysisResult:

    waveform: np.ndarray
    fs: int
    window_size: int
    hop_size: int
    fft_freqs: np.ndarray
    peroid_times: np.ndarray
    fft_max_freq:np.ndarray
    ac_max_freq:np.ndarray
    yin_freq:np.ndarray
    bedcmm_freq:np.ndarray

    frame_results: list[FrameResult]