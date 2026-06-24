import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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
