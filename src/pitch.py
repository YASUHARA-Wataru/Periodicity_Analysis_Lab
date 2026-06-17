import numpy as np


def estimate_pitch_fft(
    fft_score,
    fs,
    window_size,
    fft_freqs
):

    peak_idx = np.argmax(fft_score)
    
    return fft_freqs[peak_idx]


def estimate_pitch_ac(
    ac_score,
    fs,
    fmax
):
    tmin = int(np.floor(fs/fmax))

    peak_idx = np.argmax(ac_score)
    if peak_idx != 0:
        pitch = fs/(peak_idx+tmin)
        #pitch = fs/(peak_idx)
    else:
        pitch = np.nan

    return  pitch