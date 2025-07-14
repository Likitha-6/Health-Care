import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config("📈 BTST Screener", layout="wide")
st.title("📈 BTST Screener for Indices (Live After 3 PM)")

# List of watchlist indices
indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "SENSEX": "^BSESN"
}

# Time check
time_now = datetime.datetime.now().time()
after_3pm = time_now >= datetime.time(15, 0)

# Helper function to fetch intraday data
def fetch_index_data(symbol):
    data = yf.download(symbol, period="1d", interval="5m")
    return data

results = []

for name, symbol in indices.items():
    try:
        df = fetch_index_data(symbol)
        if df.empty or df.shape[0] < 2:
            continue

        latest = df.iloc[-1]
        day_high = df['High'].max()
        day_low = df['Low'].min()
        close_price = latest['Close']
        volume = latest['Volume'] if 'Volume' in df.columns else 0

        # Convert to scalar for comparison
        close_val = float(close_price)
        high_val = float(day_high)
        low_val = float(day_low)

        # Trend direction check
        if pd.notna(close_val) and pd.notna(high_val) and (close_val > (0.995 * high_val)):
            signal = "🔼 Possible BTST Long"
        elif pd.notna(close_val) and pd.notna(low_val) and (close_val < (1.005 * low_val)):
            signal = "🔽 Possible BTST Short"
        else:
            signal = "⏳ No clear setup"

        results.append({
            "Index": name,
            "Close": round(close_val, 2),
            "Day High": round(high_val, 2),
            "Day Low": round(low_val, 2),
            "Volume": int(volume),
            "Signal": signal
        })

    except Exception as e:
        st.error(f"Error fetching {name}: {e}")

# Display results
if after_3pm:
    if results:
        df_result = pd.DataFrame(results)
        st.dataframe(df_result)
    else:
        st.warning("No data or signals detected from selected indices.")
else:
    st.info("⏳ Waiting for 3:00 PM... Screener will activate then.")
