# Periodicity Analysis Lab
## Usage

```bash
uv sync
streamlit run app.py
```

## Dependencies

- NumPy
- librosa
- Plotly
- Streamlit
- bedcmmPitch (separate license)

## Pitch Detection Lab

Compare periodicity analysis methods:

- FFT
- Autocorrelation
- YIN (CMNDF)
- bedcmm

Features
- Waveform visualization
- Frame-by-frame analysis
- Pitch track comparison

### Main Interface
![pic_1](./pic/Pitch_Detection_Lab_0.png)
### Play and Control Panel
![pic_2](./pic/Pitch_Detection_Lab_1.png)
### Wave Form
![pic_3](./pic/Pitch_Detection_Lab_2.png)
## Periodicity Analysis
![pic_4](./pic/Pitch_Detection_Lab_3.png)
## Pitch Track Comparison
![pic_5](./pic/Pitch_Detection_Lab_4.png)

Comparison of FFT spectrum, autocorrelation, YIN CMNDF, and bedcmm periodicity score for the selected analysis frame.

## License

Periodicity Analysis Lab is released under the MIT License.

This project depends on the bedcmmPitch library, which is distributed under a separate proprietary/custom license.

Please refer to the bedcmmPitch repository for the terms and conditions of its use.

## Pitch Tracking Lab

Pitch Tracking Lab is an interactive Streamlit application for visualizing and comparing pitch tracking algorithms.

The application allows you to compare:

* bedcmm
* bedcmm + Bayes Tracking
* bedcmm + Viterbi Tracking
* YIN
* pYIN

### Features

* Upload audio files and analyze pitch trajectories.
* Compare pitch estimates from multiple algorithms.
* Visualize periodicity score maps as heatmaps.
* Overlay tracking results on the score maps.
* Inspect frame-by-frame periodicity functions.
* Explore how different tracking methods select pitch candidates over time.

The goal of this project is not only to compare the final pitch estimates, but also to visualize **why** each algorithm chooses a particular pitch trajectory.

### Example Views

* Pitch Tracking Comparison
![pic_6](pic/Pitch_Tracking_Lab1.png)
* bedcmm Score Map
![pic_6](pic/Pitch_Tracking_Lab2.png)
* YIN Score Map
![pic_6](pic/Pitch_Tracking_Lab3.png)
* Current Frame Analysis
![pic_6](pic/Pitch_Tracking_Lab4.png)


### Related Algorithms

* YIN
* pYIN
* Bayesian Tracking
* Viterbi Tracking
* bedcmm

### Purpose

This project aims to provide an intuitive way to understand pitch tracking algorithms by visualizing their internal score functions and tracking behavior.


## Reference
bedcmmPitch:
https://github.com/YASUHARA-Wataru/bedcmmPitch