import streamlit as st
import chart_module  # 🔍 전체 모듈 import (이게 핵심!)
from chart_module import generate_chart

st.set_page_config(page_title="SmartSwing Tracker", layout="wide", initial_sidebar_state="expanded")
st.title("📈 SmartSwing Tracker (DEBUG)")

# 🔎 chart_generator 모듈의 실제 파일 경로 출력
st.write("💡 현재 불러진 chart_module.py 경로:", chart_generator.__file__)

uploaded_file = st.sidebar.file_uploader("📤 credentials.json 업로드", type="json")
if uploaded_file:
    with open("credentials.json", "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success("✅ credentials.json 업로드 완료!")

ticker = "NVDA"
strategy = "RSI 반등 + MACD 골든크로스"
st.success(f"추천 종목: {ticker} / 전략: {strategy}")

with st.spinner("차트 생성 중..."):
    chart_path, error = generate_chart(ticker)
    if chart_path:
        st.image(chart_path, caption=f"{ticker} 차트")
        st.success("📊 차트 생성 완료!")
    else:
        st.error(error)
