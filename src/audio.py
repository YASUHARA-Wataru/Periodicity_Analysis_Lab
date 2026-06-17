import librosa

def load_audio(path):

    y, sr = librosa.load(
        path,
        sr=None,
        mono=True,
    )

    return y, sr