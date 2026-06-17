import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.audio import load_audio
from src.config import AnalysisConfig
from src.result import FrameResult
from src.analyze import analyze_audio


st.set_page_config(
    page_title="Pitch Detection Lab",
    layout="wide"
)

st.title("Pitch Detection Lab")


# =====================================================
# Session State
# =====================================================

if "loaded" not in st.session_state:
    st.session_state.loaded = False


# =====================================================
# Dummy Plot Functions
# =====================================================

def create_waveform_plot(y,fs,window_size,current_time):

    x = np.arange(0,len(y)/fs,1/fs)

    # 2. サブプロットの作成 (1行2列)
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("All Wave", "Analyze Area"),
        specs=[[{"type": "xy"}, {"type": "xy"}]]
    )

    # --- 左側：元のグラフ ---
    max_points = 2500
    step = max(1, len(y) // max_points)
    fig.add_trace(go.Scattergl(x=x[::step], y=y[::step], mode='lines', name='all wave'), row=1, col=1)
    
    # 四角形の座標（拡大したい領域）
    x0, x1 = current_time, current_time + (window_size/fs)
    y0, y1 = min(y), max(y)

    # 元のグラフに四角形の枠線を追加
    fig.add_shape(
        type="rect",
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color="red", width=2),
        fillcolor="rgba(255, 0, 0, 0.15)", # 半透明の赤色で塗りつぶし
        row=1, col=1
    )

    # --- 右側：拡大図 ---
    fig.add_trace(go.Scattergl(x=x, y=y, mode='lines', name='Analyze Area'), row=1, col=2)

    # 拡大図の表示範囲を四角形の範囲に合わせて固定
    fig.update_xaxes(range=[x0, x1], row=1, col=2)
    fig.update_yaxes(range=[y0, y1], row=1, col=2)

    # 3. Streamlitに描画
    st.title("Wave Form")

    fig.update_layout(
        height=250,
        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10,
        ),
        showlegend=False,
    )

    return fig


def create_method_plot(y,x,name):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=name,
        height=180,
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10,
        ),
    )

    return fig


def create_pitch_track_plot(current_time,results:FrameResult):

    x = np.arange(0,len(results.waveform)/results.fs,results.hop_size/results.fs)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=results.fft_max_freq,
            name="FFT",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=results.bedcmm_freq,
            name="bedcmm",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=results.yin_freq,
            name="YIN",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=results.ac_max_freq,
            name="Autocorrelation",
        )
    )

    fig.add_vline(
        x=(current_time - 1/results.fs*results.hop_size),
        line_width=2,
    )

    fig.update_layout(
        height=250,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10,
        ),
        legend=dict(
            orientation="h"
        )
    )

    return fig


# =====================================================
# Top Controls
# =====================================================

col_source, col_setting = st.columns(2)

with col_source:

    st.subheader("Data Source")

    source_type = st.radio(
        "Source",
        ["Sample Data", "Upload WAV"],
    )

    selected_path = None
    uploaded_file = None

    if source_type == "Sample Data":

        sample_files = [
            "data/audio/pure_220.wav",
            "data/audio/white_noise.wav",
            "data/audio/voiced_unvoiced.wav",
            "data/audio/octave_jump.wav",
            "data/audio/harmonic_220.wav",
            "data/audio/harmonic_trap.wav",
            "data/audio/spike_noise.wav",
            "data/audio/vibrato.wav",
            "data/audio/guitar_pentatonic_1.wav",
        ]

        selected_path = st.selectbox(
            "Sample File",
            sample_files,
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload WAV",
            type=["wav"],
        )


with col_setting:

    st.subheader("Analysis Settings")

    window_size = st.selectbox(
        "Window Size",
        [512, 1024, 2048, 4096, 8192],
        index=2,
    )

    hop_size = st.selectbox(
        "Hop Size",
        [128, 256, 512, 1024, 2048],
        index=2,
    )

    min_f0 = st.number_input(
        "Min F0 [Hz]",
        value=50.0,
        min_value=1.0,
    )

    max_f0 = st.number_input(
        "Max F0 [Hz]",
        value=2000.0,
        min_value=1.0,
    )

    analysis_config = AnalysisConfig(window_size=window_size,
                                     hop_size=hop_size,
                                     min_f0=min_f0,
                                     max_f0=max_f0)

    st.session_state.analysis_config = analysis_config

st.divider()

if st.button(
    "Load and Analyze",
    width='stretch',
):

    # -----------------------------
    # Parameter Check
    # -----------------------------

    if min_f0 >= max_f0:

        st.error(
            "Min F0 must be smaller than Max F0."
        )

        st.stop()

    if hop_size >= window_size:

        st.error(
            "Hop Size must be smaller than Window Size."
        )

        st.stop()
    

    # -----------------------------
    # File Check
    # -----------------------------

    if source_type == "Upload WAV":

        if uploaded_file is None:

            st.error(
                "Please select a WAV file."
            )

            st.stop()

    # -----------------------------
    # Analysis
    # -----------------------------

    with st.status(
        "Analyzing...",
        expanded=True,
    ) as status:

        st.write("Loading WAV file...")

        if source_type == "Sample Data":

            st.session_state.wave_path = selected_path

        else:

            st.session_state.wave_path = uploaded_file

        y,sr = load_audio(st.session_state.wave_path)

        MAX_DURATION = 10.0

        if len(y) / sr > MAX_DURATION:
            st.error(
                f"Audio must be shorter than {MAX_DURATION} seconds."
            )
            st.stop()

        if int(np.ceil(1/min_f0*sr)) > (window_size//2):

            st.error(
                f"fmin must be lager than {sr/(window_size//2)} Hz"
            )

            st.stop()

        st.write("Analyze audio file...")
        resutls = analyze_audio(y,sr,st.session_state.analysis_config)
        st.session_state.results = resutls

        status.update(
            label="Analysis Complete",
            state="complete",
        )

    st.session_state.loaded = True

# =====================================================
# Analysis Area
# =====================================================

if st.session_state.loaded:
    
    st.audio(
        st.session_state.wave_path
    )

    st.divider()

    st.caption(
        f"Window:{st.session_state.analysis_config.window_size}  "
        f"Hop:{st.session_state.analysis_config.hop_size}  "
        f"F0:{st.session_state.analysis_config.min_f0:.0f}-{st.session_state.analysis_config.max_f0:.0f}Hz"
    )

    results = st.session_state.results
    audio_len_sec = len(results.waveform)/results.fs
    audio_step = results.hop_size/results.fs
    max_value_minus = results.window_size/results.fs

    current_time = st.slider(
        "Current Time [s]",
        min_value=0.0,
        max_value=audio_len_sec-max_value_minus,
        value=0.0,
        step=audio_step,
    )

    st.plotly_chart(
        create_waveform_plot(results.waveform,results.fs,results.window_size,current_time),
        width='stretch',
    )

    st.divider()

    st.markdown("### Wave Analysis(FT and Periodicity)")

    fft_col, bed_col, yin_col, ac_col = st.columns(4)
    frame_idx = int(
        current_time * results.fs / results.hop_size
    )
    methods = [
        ("FFT", fft_col,results.frame_results[frame_idx].fft_score,results.fft_max_freq[frame_idx]),
        ("bedcmm", bed_col,results.frame_results[frame_idx].bedcmm_score,results.bedcmm_freq[frame_idx]),
        ("YIN(CMNDF)", yin_col,results.frame_results[frame_idx].yin_score,results.yin_freq[frame_idx]),
        ("Autocorrelation", ac_col,results.frame_results[frame_idx].ac_score,results.ac_max_freq[frame_idx]),
    ]


    for name, col , score, estimate_freq in methods:

        with col:
            if name == 'FFT':
                x = results.fft_freqs
            else:
                x = results.peroid_times

            st.plotly_chart(
                create_method_plot(score,x,name),
                width='stretch',
            )
            st.metric(
                "Frequency",
                f"{estimate_freq:.2f} Hz",
            )

    st.divider()

    st.markdown("### Pitch Track Comparison")

    st.plotly_chart(
        create_pitch_track_plot(current_time,results),
        width='stretch',
    )

else:

    st.info(
        "Select data and press 'Load and Analyze'."
    )