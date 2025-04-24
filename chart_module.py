import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        print("🚀 현재 실행 중인 chart_module.py 입니다!")

        end = datetime.today()
        start = end - timedelta(days=60)

        df = yf.download(ticker, start=start, end=end)

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if df.empty or not all(col in df.columns for col in required_columns):
            logging.warning("❌ 필요한 컬럼이 누락되었습니다.")
            return None, "❌ 데이터가 없습니다: 필요한 열이 없습니다."

        df = df[required_columns].dropna()

        # ✅ 반드시 Series로 분리
        open_series = df["Open"]
        logging.info(f"[DEBUG] Open dtype: {open_series.dtype}")
        logging.info(f"[DEBUG] Open values (head):\n{open_series.head()}")
        logging.info(f"[DEBUG] Open types:\n{[type(x) for x in open_series.head()]}")

        df = df.astype("float64").copy()
        df.index.name = "Date"

        chart_path = f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}_chart.png"
        mpf.plot(
            df,
            type="candle",
            mav=(5, 20),
            volume=True,
            style="yahoo",
            savefig=chart_path
        )

        logging.info(f"✅ 차트 생성 완료: {chart_path}")
        return chart_path, None

    except Exception as e:
        logging.error(f"차트 생성 중 예외 발생: {str(e)}")
        return None, f"❌ 차트 생성 실패: {str(e)}"
