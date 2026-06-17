import numpy as np
from src.result import (
    AnalysisResult,
    FrameResult,
)
from src.config import AnalysisConfig
from src.periodicity import calc_fft,calc_yin_cmndf,calc_autocorrelation,get_fft_freqs,get_peroid_times
from src.pitch import estimate_pitch_fft,estimate_pitch_ac
import bedcmmPitch
import librosa

def analyze_audio(y, fs,AnalysisConfig:AnalysisConfig):

    frame_results = []

    window_size = AnalysisConfig.window_size
    hop_size = AnalysisConfig.hop_size
    fmin = AnalysisConfig.min_f0
    fmax = AnalysisConfig.max_f0
    frames = np.arange(window_size,len(y),hop_size)

    fft_freqs = get_fft_freqs(window_size,fs,fmin,fmax)
    peroid_times = get_peroid_times(window_size,fs,fmin,fmax)

    fft_max_freq_list = []
    ac_max_freq_list = []
    yin_freq_list = librosa.yin(y=y,sr=fs,fmin=fmin,fmax=fmax,frame_length=window_size,hop_length=hop_size,center=False)

    bedcmm_score_list,_ = bedcmmPitch.calc_bedcmm(y,fs=fs,window_size=window_size,hop_size=hop_size,fmin=fmin,fmax=fmax)
    bedcmm_freq_list,_ = bedcmmPitch.calc_Pitch(y,fs=fs,window_size=window_size,hop_size=hop_size,fmin=fmin,fmax=fmax)

    for idx,frame in enumerate(frames):
        y_frame = y[frame-window_size:frame]

        fft_score = calc_fft(y_frame,fs,window_size,fmin,fmax)/(window_size/2)
        ac_score = calc_autocorrelation(y_frame,fs,window_size,fmin,fmax)
        yin_score = calc_yin_cmndf(y_frame,fs,fmin,fmax)
        bedcmm_score = bedcmm_score_list[idx]
        
        fft_max_freq = estimate_pitch_fft(fft_score,fs,window_size,fft_freqs)
        ac_max_freq = estimate_pitch_ac(ac_score,fs,fmax)

        frame_result = FrameResult(
            fft_score=fft_score,
            ac_score=ac_score,
            yin_score=yin_score,
            bedcmm_score=bedcmm_score,
        )

        frame_results.append(
            frame_result
        )
        fft_max_freq_list.append(fft_max_freq)
        ac_max_freq_list.append(ac_max_freq)

    return AnalysisResult(
        waveform=y,
        fs=fs,
        window_size=window_size,
        hop_size=hop_size,
        fft_freqs=fft_freqs,
        peroid_times=peroid_times,
        frame_results=frame_results,
        fft_max_freq=fft_max_freq_list,
        ac_max_freq=ac_max_freq_list,
        yin_freq=yin_freq_list,
        bedcmm_freq=bedcmm_freq_list
    )