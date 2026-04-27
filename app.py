import feedparser
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="stock_refresh")

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# Multi-stock selection
stocks = st.multiselect(
    "Select Stocks to Compare",
    ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"],
    default=["AAPL", "TSLA"]
)

# Build comparison data
comparison_data = pd.DataFrame()

for stock in stocks:
    df = yf.Ticker(stock).history(period="1mo")
    comparison_data[stock] = df["Close"]

# Show comparison chart
st.subheader("Stock Comparison")
st.line_chart(comparison_data)

# ---- Optional: show metrics for FIRST selected stock ----
if stocks:
    selected_stock = stocks[0]
    data = yf.Ticker(selected_stock).history(period="6mo")

    latest = data.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Current Price", f"${latest['Close']:.2f}")
    col2.metric("High", f"${latest['High']:.2f}")
    col3.metric("Low", f"${latest['Low']:.2f}")
    col4.metric("Volume", f"{int(latest['Volume']):,}")

    # SMA
    data["SMA20"] = data["Close"].rolling(20).mean()

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], name="SMA20"))

    fig.update_layout(title=f"{selected_stock} Price Chart")

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📰 Latest Market News")

news = feedparser.parse("https://finance.yahoo.com/rss/topstories")

for entry in news.entries[:5]:
    st.write("**" + entry.title + "**")
    st.write(entry.link)
    st.write("---")