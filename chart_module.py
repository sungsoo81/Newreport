import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging
import traceback

logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        print("🚀 chart_module.py 실행 중")

        end = datetime.today()
        start = end - timedelta(days=60)

        print("📍 1단계: 데이터 다운로드 시작")
        df = yf.download(ticker, start=start, end=end)
        print("✅ 1단계 완료")

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if df.empty or not all(col in df.columns for col in required_columns):
            logging.warning("❌ 필요한 컬럼이 누락되었습니다.")
            return None, "❌ 데이터가 없습니다: 필요한 열이 없습니다."

        print("📍 2단계: 필수 컬럼 추출 및 결측치 제거")
        df = df[required_columns].dropna()
        print("✅ 2단계 완료")

        try:
            print("📍 3단계: Series 분리")
            open_series = df["Open"]
            print("✅ open_series 생성됨")
        except Exception as e:
            print("❌ open_series 생성 실패:", e)
            traceback.print_exc()
            return None, f"❌ open_series 생성 실패: {str(e)}"

        try:
            print("📍 4단계: dtype 읽기")
            dtype = open_series.dtypes
            print("✅ dtype:", dtype)
        except Exception as e:
            print("❌ dtype 읽기 실패:", e)
            traceback.print_exc()
            return None, f"❌ dtype 읽기 실패: {str(e)}"

        try:
            print("📍 5단계: float64 변환")
            df = df.astype("float64").copy()
            df.index.name = "Date"
            print("✅ 5단계 완료")
        except Exception as e:
            print("❌ float64 변환 실패:", e)
            traceback.print_exc()
            return None, f"❌ 변환 실패: {str(e)}"

        chart_path = f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}_chart.png"

        try:
            print("📍 6단계: 차트 생성 시도")
            mpf.plot(
                df,
                type="candle",
                mav=(5, 20),
                volume=True,
                style="yahoo",
                savefig=chart_path
            )
            print("✅ 6단계 완료: 차트 생성됨")
        except Exception as e:
            print("❌ 차트 생성 중 오류:", e)
            traceback.print_exc()
            return None, f"❌ 차트 생성 실패: {str(e)}"

        logging.info(f"✅ 차트 생성 완료: {chart_path}")
        return chart_path, None

    except Exception as e:
        logging.error("차트 생성 전체 실패")
        traceback.print_exc()
        return None, f"❌ chart_module 전체 실패: {str(e)}"
