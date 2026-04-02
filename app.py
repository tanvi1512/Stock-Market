import streamlit as st
import matplotlib.pyplot as plt
import requests
from model import train_model, predict_next_day

# 🔑 API KEY
API_KEY = "d77575pr01qtg3nflv00d77575pr01qtg3nflv0g"

st.set_page_config(page_title="Stock Predictor Pro", layout="wide")

# 🌙 Dark UI
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3, h4, h5, h6, label {
    color: white !important;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 3em;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# 🔥 HEADER
st.markdown("<h2 style='text-align:center;'>📈 Stock Predictor Pro</h2>", unsafe_allow_html=True)

# 📊 STOCK LIST
stocks = {
    "Apple": "AAPL", "Tesla": "TSLA", "Microsoft": "MSFT",
    "Google": "GOOGL", "Amazon": "AMZN",
    "Reliance": "RELIANCE.NS", "TCS": "TCS.NS",
    "Infosys": "INFY.NS", "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS", "SBI": "SBIN.NS"
}

# 🧩 Layout
left, right = st.columns([1, 2])

# 🔍 INPUT SECTION
with left:
    st.subheader("🔎 Input Section")

    query = st.text_input("🔍 Search stock (API)")

    # Disable dropdown if search is used
    dropdown_disabled = True if query else False

    selected_name = st.selectbox(
        "📊 Select from list",
        list(stocks.keys()),
        disabled=dropdown_disabled
    )

    dropdown_stock = stocks[selected_name]

    # 🔎 API search function
    def search_stock(q):
        url = f"https://finnhub.io/api/v1/search?q={q}&token={API_KEY}"
        return requests.get(url).json().get("result", [])

    selected_stock = None

    if query:
        results = search_stock(query)
        if results:
            options = [f"{r['description']} ({r['symbol']})" for r in results[:5]]
            choice = st.selectbox("Results", options)
            selected_stock = choice.split("(")[-1].replace(")", "")
        else:
            st.warning("No results found")

    # Final stock selection
    stock = selected_stock if selected_stock else dropdown_stock

    st.write(f"**Selected:** {stock}")

    run = st.button("🚀 Predict")

# 📊 OUTPUT SECTION
with right:
    if run:
        try:
            st.info(f"Fetching data for: {stock}")

            model, acc, data = train_model(stock)

            col1, col2 = st.columns(2)

            # 📈 GRAPH
            with col1:
                st.subheader("📊 Price Trend")

                fig, ax = plt.subplots()
                close_prices = data['Close'].values

                for i in range(1, len(close_prices)):
                    if close_prices[i] > close_prices[i-1]:
                        ax.plot([i-1, i], [close_prices[i-1], close_prices[i]],
                                color="lime", linewidth=2)
                    else:
                        ax.plot([i-1, i], [close_prices[i-1], close_prices[i]],
                                color="red", linewidth=2)

                ax.set_facecolor("#0e1117")
                fig.patch.set_facecolor("#0e1117")

                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                for spine in ax.spines.values():
                    spine.set_color('white')
                    spine.set_linewidth(1.5)

                ax.set_title("Stock Price Movement", color='white')
                ax.set_xlabel("Time", color='white')
                ax.set_ylabel("Price", color='white')

                st.pyplot(fig)

            # 📊 MARKET INSIGHT
            with col2:
                st.subheader("📊 Market Insight")

                today = data['Close'].iloc[-2]
                tomorrow = data['Close'].iloc[-1]
                pct_change = ((tomorrow - today) / today) * 100

                if pct_change > 0:
                    st.markdown(
                        f"<h1 style='color:lime;'>📈 +{pct_change:.2f}%</h1>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<h1 style='color:red;'>📉 {pct_change:.2f}%</h1>",
                        unsafe_allow_html=True
                    )

                # 🔮 Prediction
                pred = predict_next_day(model, data)

                st.subheader("🔮 Prediction")

                if pred == 1:
                    st.success("📈 UP → BUY")
                else:
                    st.error("📉 DOWN → SELL")

        except Exception as e:
            st.error(str(e))