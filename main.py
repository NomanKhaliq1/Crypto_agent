
import streamlit as st
import requests
import pandas as pd
import time


st.set_page_config(page_title="💰 Crypto Agent", layout="wide")
st.title("💰 Crypto Agent")
st.caption("Live crypto prices • Portfolio tracking • Comparison tool")


@st.cache_data(ttl=60)
def get_price(symbol: str):
    """Fetch current price from CoinGecko API (cached for 60s)."""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": symbol, "vs_currencies": "usd"}
    try:
        res = requests.get(url, params=params, timeout=10).json()
        return res.get(symbol, {}).get("usd", None)
    except Exception:
        return None

def format_usd(val):
    return f"${val:,.2f}"

def format_pkr(val):
    return f"Rs {val*280:,.0f}"  


if "portfolio" not in st.session_state:
    st.session_state.portfolio = []  


st.sidebar.header("➕ Add to Portfolio")
coin = st.sidebar.text_input("Coin ID (e.g. bitcoin, ethereum, dogecoin)")
amount = st.sidebar.number_input("Amount you hold", min_value=0.0, step=0.01)
if st.sidebar.button("Add"):
    if coin and amount > 0:
        st.session_state.portfolio.append({"symbol": coin.lower(), "amount": amount})


if st.session_state.portfolio:
    st.subheader("📊 Your Portfolio")
    rows = []
    total_value = 0
    for item in st.session_state.portfolio:
        price = get_price(item["symbol"])
        if price:
            value = price * item["amount"]
            total_value += value
            rows.append({
                "Coin": item["symbol"],
                "Amount": item["amount"],
                "Price (USD)": format_usd(price),
                "Value (USD)": format_usd(value),
                "Value (PKR)": format_pkr(value)
            })
    df = pd.DataFrame(rows)
    st.table(df)
    st.success(f"💼 Total Portfolio Value: {format_usd(total_value)} | {format_pkr(total_value)}")
else:
    st.info("Add coins to your portfolio from the sidebar.")



st.subheader("⚖️ Price Comparison")
coins = st.text_input("Enter coin IDs (comma-separated)", "bitcoin, ethereum, dogecoin")
if st.button("Compare"):
    ids = [c.strip() for c in coins.split(",")]
    data = []
    for c in ids:
        price = get_price(c)
        if price:
            data.append({"Coin": c, "Price (USD)": format_usd(price), "Price (PKR)": format_pkr(price)})
    if data:
        st.dataframe(pd.DataFrame(data))
