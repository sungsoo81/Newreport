import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging
import traceback

logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        print("🚀 chart_module_nanproof_final.py 실행 시작")

        end = datetime.today()
        start = end - timedelta(days=60)

        print("📍 1단계: 데이터 다운로드")
        df = yf.download(ticker, start=start, end=end)
        print("✅ 다운로드 완료")

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        print("📎 현재 DataFrame 컬럼:", df.columns.tolist())

        if df.empty or not all(col in df.columns for col in required_columns):
            missing = set(required_columns) - set(df.columns)
            logging.warning(f"❌ 필요한 컬럼 누락: {missing}")
            return None, f"❌ 데이터 누락: {missing}"

        df = df[[col for col in required_columns if col in df.columns]]

        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except Exception as e:
                print(f"⚠️ {col} 변환 실패: {e}")

        # ✅ NaN-only 컬럼 제거
        existing_cols = [col for col in required_columns if col in df.columns and not df[col].isna().all()]
        print("🧪 NaN-only 제거 후 dropna 대상 컬럼:", existing_cols)

        # 진단 로그
        for col in required_columns:
            print(f"🔍 {col} in df.columns: {col in df.columns}")
            if col in df:
                print(f"    → type: {type(df[col])}, NaN 비율: {df[col].isna().mean():.2%}")

        if existing_cols:
            df.dropna(subset=existing_cols, inplace=True)
        else:
            return None, "❌ 유효한 컬럼이 전혀 없어 dropna 불가"

        df = df.astype("float64").copy()
        df.index.name = "Date"

        print("📍 클렌징 완료 후 DataFrame 상태:")
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
