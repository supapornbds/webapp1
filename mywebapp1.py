import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from streamlit_bokeh import streamlit_bokeh

SPREADSHEET_ID = "1oc92J5K6TuJr5neTF4hri3aoKB5OmHxuWIY2TC0e2D8"
SHEET_NAME     = "Sheet1"

@st.cache_data(ttl=10)
def load_sheet():
    """
    โหลดข้อมูลจาก Google Sheet
    คอลัมน์:
      0 -> timestamp (รูปแบบ d/m/Y, H:M:S)
      1 -> temp       (°C)
      2 -> humidity   (%)
    """
    csv_url = (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )

    df = pd.read_csv(csv_url, header=None, names=['timestamp', 'temp', 'humidity'])
    # แปลงเป็น datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
    return df

@st.cache_resource
def init_chart():
    """เตรียม Bokeh figure และ ColumnDataSource"""
    source = ColumnDataSource(data=dict(timestamp=[], temp=[], humidity=[]))
    p = figure(
        title="Realtime Temperature & Humidity",
        x_axis_type='datetime',
        width=700,
        height=400
    )
    p.line('timestamp', 'temp',color="#ff0000",source=source, line_width=2, legend_label="Temperature (°C)")
    p.line('timestamp', 'humidity',color="#00ff00",source=source, line_width=2, legend_label="Humidity (%)")
    p.legend.location = 'top_left'
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Value'
    return p, source

st.title("กราฟ Temperature & Humidity จาก Google Sheet")

p, source = init_chart()

# อัปเดตข้อมูลในกราฟทุก 10 วินาที
@st.fragment(run_every="10s")
def display_realtime():
    df = load_sheet()
    source.data = {
        'timestamp': df['timestamp'],
        'temp':      df['temp'],
        'humidity':  df['humidity']
    }
    streamlit_bokeh(p, use_container_width=True, theme="streamlit", key="plot")

display_realtime()
