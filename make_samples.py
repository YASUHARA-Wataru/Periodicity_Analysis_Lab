import os
import numpy as np
from scipy.io.wavfile import write

FS = 44100

os.makedirs("data/audio/", exist_ok=True)


def save_wav(name, x):
    x = x / np.max(np.abs(x))
    write(
        f"data/audio/{name}.wav",
        FS,
        x.astype(np.float32)
    )


def harmonic_signal(
    f0,
    duration,
    harmonics=(1.0,),
):
    t = np.arange(int(duration * FS)) / FS

    x = np.zeros_like(t)

    for k, amp in enumerate(harmonics, start=1):
        x += amp * np.sin(
            2*np.pi*k*f0*t
        )

    return x


def add_white_noise(
    x,
    noise_level,
):
    return x + noise_level*np.random.randn(len(x))


def add_spike_noise(
    x,
    spike_rate=0.001,
    spike_amplitude=2.0,
):
    y = x.copy()

    n_spikes = int(len(x)*spike_rate)

    idx = np.random.choice(
        len(x),
        n_spikes,
        replace=False
    )

    signs = np.random.choice(
        [-1, 1],
        n_spikes
    )

    y[idx] += spike_amplitude*signs

    return y


def vibrato_signal(
    f0,
    duration,
    rate=5,
    depth=0.03,
):
    t = np.arange(int(duration*FS))/FS

    f = f0 * (
        1 + depth*np.sin(
            2*np.pi*rate*t
        )
    )

    phase = 2*np.pi*np.cumsum(f)/FS

    return np.sin(phase)


def chirp_signal(
    f_start,
    f_end,
    duration,
):
    t = np.arange(int(duration*FS))/FS

    f = np.linspace(
        f_start,
        f_end,
        len(t)
    )

    phase = 2*np.pi*np.cumsum(f)/FS

    return np.sin(phase)


# -------------------------
# 生成
# -------------------------
np.random.seed(42)

save_wav(
    "pure_220",
    harmonic_signal(
        220,
        5,
        (1.0,)
    )
)

save_wav(
    "harmonic_220",
    harmonic_signal(
        220,
        5,
        (1.0,0.5,0.25)
    )
)

save_wav(
    "harmonic_trap",
    harmonic_signal(
        220,
        5,
        (0.3,1.0,0.8)
    )
)

save_wav(
    "white_noise",
    add_white_noise(
        harmonic_signal(
            220,
            5,
            (1.0,0.5)
        ),
        0.05
    )
)

save_wav(
    "spike_noise",
    add_spike_noise(
        harmonic_signal(
            220,
            5,
            (1.0,0.5)
        ),
        spike_rate=0.01,
        spike_amplitude=5.0
    )
)

save_wav(
    "vibrato",
    vibrato_signal(
        220,
        5
    )
)

save_wav(
    "chirp_100_400",
    chirp_signal(
        100,
        400,
        5
    )
)

save_wav(
    "octave_jump",
    np.concatenate([
        harmonic_signal(
            220,
            2.5,
            (1.0,0.5)
        ),
        harmonic_signal(
            440,
            2.0,
            (1.0,0.5)
        ),
        harmonic_signal(
            220,
            2.5,
            (1.0,0.5)
        )
    ])
)

save_wav(
    "voiced_unvoiced",
    np.concatenate([
        harmonic_signal(
            220,
            2
        ),
        np.zeros(FS),
        harmonic_signal(
            220,
            2
        )
    ])
)

print("done")