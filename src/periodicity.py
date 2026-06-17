import numpy as np


def get_fft_freqs(window_size,fs,fmin,fmax):

    fft_freqs = np.fft.rfftfreq(window_size,1/fs)
    fft_freqs = fft_freqs[(fft_freqs > fmin) & (fft_freqs < fmax)]

    return fft_freqs

def get_peroid_times(window_size,fs,fmin,fmax):
    
    peroid_times = np.arange(1/fs,(window_size//2)/fs,1/fs)
    peroid_times = peroid_times[(1/peroid_times > fmin) & (1/peroid_times < fmax)]
    return peroid_times



def calc_fft(frame,fs,window_size,fmin,fmax):

    freqs = np.fft.rfftfreq(window_size,1/fs)

    fft = np.abs(
        np.fft.rfft(frame)
    )[(freqs > fmin) & (freqs < fmax)]

    return fft


def calc_autocorrelation(frame,fs,window_size,fmin,fmax):
    
    frame = frame - np.mean(frame)

    ac = np.correlate(
        frame,
        frame,
        mode="full"
    )

    tmin = int(np.floor(fs/fmax))
    tmax = int(np.ceil(fs/fmin))
    
    ac = ac[len(ac)//2:-len(ac)//4]
    ac /= ac[0]
    ac = ac[tmin:tmax+1]

    return ac

def calc_yin_cmndf(frame,fs,fmin,fmax):

    tmin = int(np.floor(fs/fmax))
    tmax = int(np.ceil(fs/fmin))

    diff = np.zeros(tmax + 1)

    for tau in range(1, tmax + 1):

        delta = frame[:-tau] - frame[tau:]

        diff[tau] = np.sum(delta**2)

    cmndf = np.ones_like(diff)

    cumulative = 0.0

    for tau in range(1, tmax + 1):

        cumulative += diff[tau]

        if cumulative > 0:

            cmndf[tau] = diff[tau] * tau / cumulative

    return cmndf[tmin:tmax+1]