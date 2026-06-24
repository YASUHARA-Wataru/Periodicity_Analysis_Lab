import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.audio import load_audio
from src.config import AnalysisConfig
from src.result import FrameResult
from src.analyze import analyze_audio_tracking
from src.plot import create_method_plot,create_waveform_plot

st.set_page_config(
    page_title="Pitch Tracking Lab",
    layout="wide"
)

st.title("Pitch Tracking Lab")


# =====================================================
# Session State
# =====================================================

if "loaded" not in st.session_state:
    st.session_state.loaded_tracking = False


def create_pitch_track_plot(current_time,results:FrameResult):

    x = np.arange(0,len(results.waveform)/results.fs,results.hop_size/results.fs)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=results.bedcmm_freq,
                             name="bedcmm"))

    fig.add_trace(go.Scatter(x=x, y=results.bedcmm_bayes_freq,
                             name="Bayes"))

    fig.add_trace(go.Scatter(x=x, y=results.bedcmm_viterbi_freq,
                             name="Viterbi"))

    fig.add_trace(go.Scatter(x=x, y=results.yin_freq,
                             name="YIN"))

    fig.add_trace(go.Scatter(x=x, y=results.pyin_freq,
                             name="pYIN"))

    fig.add_vline(
        x=(current_time - 1/results.fs*results.hop_size),
        line_width=2,
    )

    fig.update_layout(
        height=350,
        title="Pitch Tracking Comparison"
    )

    return fig

def create_heatmap(score_map, periods, tracks, names, title,time_axis):

    fig = go.Figure()
    t = time_axis

    fig.add_trace(
        go.Heatmap(
            z=score_map.T,
            x=t,
            y=periods,
            colorscale="gray"
        )
    )


    for y, name in zip(tracks, names):

        fig.add_trace(
            go.Scatter(
                x=t,
                y=y,
                mode="lines",
                name=name
            )
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    fig.update_layout(
        height=400,
        title=title
    )

    return fig




# =====================================================
# Top Controls
# =====================================================

col_source, col_setting1,col_setting2 = st.columns(3)

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


with col_setting1:

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

with col_setting2:

    st.subheader("Analysis Settings")

    st.subheader("Bayes Tracking")

    alpha = st.number_input(
        "alpha",
        value=0.7
    )

    bayes_sigma = st.number_input(
        "bayes_sigma",
        value=0.1
    )

    st.subheader("Viterbi Tracking")

    beta = st.number_input(
        "beta",
        value=10.0
    )

    viterbi_sigma = st.number_input(
        "viterbi_sigma",
        value=0.1
    )

    analysis_config_tracking = AnalysisConfig(window_size=window_size,
                                     hop_size=hop_size,
                                     min_f0=min_f0,
                                     max_f0=max_f0,
                                     bayes_alpha=alpha,
                                     bayes_sigma=bayes_sigma,
                                     viterbi_beta=beta,
                                     viterbi_sigma=viterbi_sigma)

    st.session_state.analysis_config_tracking = analysis_config_tracking

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

            st.session_state.wave_path_tracking = selected_path

        else:

            st.session_state.wave_path_tracking = uploaded_file

        y,sr = load_audio(st.session_state.wave_path_tracking)

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
        results = analyze_audio_tracking(y,sr,st.session_state.analysis_config_tracking)
        st.session_state.results_tracking = results

        status.update(
            label="Analysis Complete",
            state="complete",
        )

    st.session_state.loaded_tracking = True

# =====================================================
# Analysis Area
# =====================================================

if st.session_state.loaded_tracking:
    
    st.audio(
        st.session_state.wave_path_tracking
    )

    st.divider()

    st.caption(
        f"Window:{st.session_state.analysis_config_tracking.window_size}  "
        f"Hop:{st.session_state.analysis_config_tracking.hop_size}  "
        f"F0:{st.session_state.analysis_config_tracking.min_f0:.0f}-{st.session_state.analysis_config_tracking.max_f0:.0f}Hz"
    )

    results = st.session_state.results_tracking
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

    st.markdown("### Pitch Track Comparison")

    st.plotly_chart(
        create_pitch_track_plot(current_time,results),
        width='stretch',
    )
    st.divider()
    time_axis = np.arange(
    0,
    len(results.waveform)/results.fs,
    results.hop_size/results.fs
    )
    track_names_list = ['bedcmm','bedcmm bayes','bedcmm viterbi']
    tracks = [1/results.bedcmm_freq,
              1/results.bedcmm_bayes_freq,
              1/results.bedcmm_viterbi_freq]
    st.plotly_chart(
        create_heatmap(results.bedcmm_score_map,results.peroid_times, tracks,track_names_list,'bedcmm score map',time_axis),
        width='stretch',
    )

    st.divider()

    track_names_list = ['YIN','pYIN']
    tracks = [1/results.yin_freq,
              1/results.pyin_freq,
              ]
    st.plotly_chart(
        create_heatmap(results.yin_score_map,results.peroid_times, tracks,track_names_list,'YIN score map',time_axis),
        width='stretch',
    )


    st.divider()
    st.markdown("### Wave Analysis(FT and Periodicity)")

    bed_col, yin_col = st.columns(2)
    frame_idx = int(
        current_time * results.fs / results.hop_size
    )
    methods = [
        ("bedcmm", bed_col,results.bedcmm_score_map[frame_idx],results.bedcmm_freq[frame_idx]),
        ("YIN(CMNDF)", yin_col,results.yin_score_map[frame_idx],results.yin_freq[frame_idx]),
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

else:

    st.info(
        "Select data and press 'Load and Analyze'."
    )