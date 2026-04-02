 📈**Stock Price Direction Predictor (ML + Streamlit)**

A machine learning-based web application that predicts whether a stock's price will go **UP 📈 or DOWN 📉** the next trading day, along with real-time stock search and visualization.

---

 **Features**

- 🔍 *Search any stock* using API (Finnhub)
- 📊 *Dropdown of popular stocks*
- 📈 *Stock price trend visualization* (Red/Green)
- 💹 *Daily % change highlighted*
- 🧠 *ML-based prediction (UP / DOWN)*
- 🌙 *Dark themed professional UI*
- ⚡ *Fast and interactive Streamlit app

---

**Machine Learning Model**

- Algorithm: **Logistic Regression**
- Type: **Classification**
- Predicts:
  - `1 → UP`
  - `0 → DOWN`
---

**How It Works**

1. User selects or searches a stock
2. Data is fetched using `yfinance`
3. Features used:
   - Close price
   - Volume
4. Model predicts next-day direction
5. App displays:
   - 📈 Trend graph
   - 💹 Daily % change
   - 🔮 Prediction (BUY / SELL)

---

**Formula Used**

Daily percentage change is calculated as:

((Today Price - Yesterday Price) / Yesterday Price) * 100


---

**🛠️ Tech Stack**

- Python 🐍
- Streamlit 
- Scikit-learn 🤖
- yFinance 📊
- Finnhub API 🔍
- Matplotlib 📈
