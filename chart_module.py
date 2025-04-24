import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging
import traceback

logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        print("🚀 chart_module_keyerror_safe.py 실행 시작")

        end = datetime.today()
        start = end - timedelta(days=60)

        print("📍 1단계: 데이터 다운로드")
        df = yf.download(ticker, start=start, end=end)
        print("✅ 다운로드 완료")

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df_columns = df.columns.tolist()
        print("📎 다운로드된 컬럼:", df_columns)

        if df.empty or not all(col in df.columns for col in required_columns):
            logging.warning("❌ 필요한 컬럼이 누락되었습니다.")
            return None, f"❌ 데이터 누락: {set(required_columns) - set(df.columns)}"

        df = df[required_columns]

        # ✅ 2단계: 수치형 강제 변환
        for col in required_columns:
            if col in df.columns and isinstance(df[col], pd.Series):
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception as e:
                    print(f"⚠️ {col} 변환 실패: {e}")
            else:
                print(f"⚠️ {col} 은 Series 아님 또는 존재하지 않음")

        # ✅ 3단계: 컬럼 존재 여부 확인 후 dropna
        existing_cols = [col for col in required_columns if col in df.columns]
        df.dropna(subset=existing_cols, inplace=True)
        df = df.astype("float64").copy()
        df.index.name = "Date"

        print("📍 클렌징 완료 후 dtype 확인:")
        print(df.dtypes)
        print(df.head())

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
        logging.error("차트 생성 실패")
        traceback.print_exc()
        return None, f"❌ 차트 생성 실패: {str(e)}"
