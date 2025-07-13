import streamlit as st
import datetime
import yfinance as yf

# Utility to get current spot and basic level logic
def get_spot_data(ticker):
    df = yf.download(ticker, period="1d", interval="5m")
    if df.empty:
        return None, (None, None)
    current = df['Close'].iloc[-1]
    day_high = df['High'].max()
    day_low = df['Low'].min()
    return current, (day_high, day_low)

# Setup
st.set_page_config("📊 Live Option Signal Dashboard", layout="wide")
st.title("📊 Live Option Signal Dashboard: Nifty, Bank Nifty & Sensex")

# Index configs
index_map = {
    "NIFTY": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "SENSEX": "^BSESN"
}

selected_index = st.selectbox("Select Index", list(index_map.keys()))
symbol = index_map[selected_index]

# Get live data
price, (day_high, day_low) = get_spot_data(symbol)

try:
    price = float(price)
    day_high = float(day_high)
    day_low = float(day_low)
except (TypeError, ValueError):
    st.error("⚠️ Invalid data received. Data might be unavailable or corrupted.")
    st.stop()

st.metric(f"📈 {selected_index} Spot", f"{price:.2f}")
st.markdown(f"**High:** {day_high:.2f}  **Low:** {day_low:.2f}")

# Support and Resistance Display
support1 = day_low
resistance1 = day_high
support2 = support1 - (resistance1 - support1) * 0.5
resistance2 = resistance1 + (resistance1 - support1) * 0.5

st.subheader("📌 Support & Resistance Levels")
st.markdown(f"- **Resistance 2:** {resistance2:.2f}")
st.markdown(f"- **Resistance 1 (Day High):** {resistance1:.2f}")
st.markdown(f"- **Support 1 (Day Low):** {support1:.2f}")
st.markdown(f"- **Support 2:** {support2:.2f}")

# Strategy logic (dynamic strikes based on ATM)
atm_strike = round(price / 50) * 50 if "NIFTY" in selected_index else round(price / 100) * 100
bearish_sell = atm_strike + 100
bearish_buy = atm_strike + 200
bullish_sell = atm_strike - 100
bullish_buy = atm_strike - 200

midpoint = (day_high + day_low) / 2
current_time = datetime.datetime.now().time()

st.subheader("🔔 Suggested Option Strategy")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⛳ Bearish Setup")
    st.write(f"**Sell** {bearish_sell} CE")
    st.write(f"**Buy** {bearish_buy} CE (Hedge)")
    st.write("Target: ₹20–30 Net Credit")
    st.write("Exit if Index crosses resistance or CE doubles")
    if current_time >= datetime.time(13, 0):
        if price > midpoint:
            st.success("✅ Favorable zone for Bearish Setup (price closer to resistance)")
        else:
            st.warning("⚠️ Price not near resistance — bearish setup not ideal")
    else:
        st.info("ℹ️ Wait until 1 PM for bearish setup checks")

with col2:
    st.markdown("### 🔻 Bullish Setup")
    st.write(f"**Sell** {bullish_sell} PE")
    st.write(f"**Buy** {bullish_buy} PE (Hedge)")
    st.write("Target: ₹20–30 Net Credit")
    st.write("Exit if Index breaks down or PE doubles")
    if current_time >= datetime.time(13, 0):
        if price < midpoint:
            st.success("✅ Favorable zone for Bullish Setup (price closer to support)")
        else:
            st.warning("⚠️ Price not near support — bullish setup not ideal")
    else:
        st.info("ℹ️ Wait until 1 PM for bullish setup checks")

# Breakout logic
st.subheader("📊 Breakout Watch")
if current_time >= datetime.time(13, 0):
    if price > day_high:
        st.success("🚀 Breakout UP! Consider Call Buy or Bull Spread")
    elif price < day_low:
        st.error("📉 Breakdown! Consider Put Buy or Bear Spread")
    else:
        st.info("No breakout yet. Monitoring post 1 PM...")
else:
    st.warning("Waiting for 1 PM to activate breakout monitoring...")

st.caption("📌 Auto-suggests ATM-based spreads. Prices shown are indicative. Use with live option chain data.")
