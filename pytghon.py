import streamlit as st
import datetime
import yfinance as yf

# Utility to get current spot and basic level logic
def get_spot_data(ticker):
    df = yf.download(ticker, period="1d", interval="5m")
    if df.empty:
        return None, None
    current = df['Close'].iloc[-1]
    day_high = df['High'].max()
    day_low = df['Low'].min()
    return current, (day_high, day_low)

# Setup
st.set_page_config("📊 Live Option Signal Dashboard", layout="wide")
st.title("📊 Live Option Signal Dashboard: Nifty & Bank Nifty")

# Index configs
index_map = {
    "NIFTY": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
}

selected_index = st.selectbox("Select Index", list(index_map.keys()))
symbol = index_map[selected_index]

# Get live data
price, (day_high, day_low) = get_spot_data(symbol)

if price is None:
    st.error("⚠️ Could not fetch live data. Try again later.")
    st.stop()

try:
    st.metric(f"📈 {selected_index} Spot", f"{float(price):.2f}")
    st.markdown(f"**High:** {float(day_high):.2f}  **Low:** {float(day_low):.2f}")
except:
    st.error("⚠️ Error in formatting live price values. Data might be incomplete or delayed.")
    st.stop()

st.markdown(f"**High:** {day_high:.2f}  **Low:** {day_low:.2f}")

# Strategy logic
atm_strike = round(price / 50) * 50 if "NIFTY" in selected_index else round(price / 100) * 100
sell_ce = atm_strike + 100
sell_pe = atm_strike - 100

st.subheader("🔔 Suggested Option Strategy")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⛳ Bearish Setup")
    st.write(f"**Sell** {sell_ce} CE")
    st.write(f"**Buy** {sell_ce + 100} CE (Hedge)")
    st.write("Target: ₹20–30 Net Credit")
    st.write("Exit if Index crosses resistance or CE doubles")

with col2:
    st.markdown("### 🔻 Bullish Setup")
    st.write(f"**Sell** {sell_pe} PE")
    st.write(f"**Buy** {sell_pe - 100} PE (Hedge)")
    st.write("Target: ₹20–30 Net Credit")
    st.write("Exit if Index breaks down or PE doubles")

# Breakout logic
st.subheader("📊 Breakout Watch")
now = datetime.datetime.now().time()
if now >= datetime.time(13, 0):
    if price > day_high:
        st.success("🚀 Breakout UP! Consider Call Buy or Bull Spread")
    elif price < day_low:
        st.error("📉 Breakdown! Consider Put Buy or Bear Spread")
    else:
        st.info("No breakout yet. Monitoring post 1 PM...")
else:
    st.warning("Waiting for 1 PM to activate breakout monitoring...")

st.caption("📌 Auto-suggests ATM-based spreads. Prices shown are indicative. Use with live option chain data.")
