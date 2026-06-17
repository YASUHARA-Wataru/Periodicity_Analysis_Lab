import streamlit as st

st.set_page_config(
    page_title="Periodicity Analysis Lab",
    page_icon="🎵",
    layout="wide"
)

st.title("Periodicity Analysis Lab")

st.markdown(
    """
    This application visualizes periodicity analysis methods
    used for pitch detection and pitch tracking.

    ### Available Pages

    - Pitch Detection Lab
    - Pitch Tracking Lab (Coming Soon)
    - Periodicity Explorer (Coming Soon)

    Select a page from the sidebar.
    """
)