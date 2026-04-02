import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def get_data(stock):
    data = yf.download(stock, start="2015-01-01", end="2024-01-01")

    if data.empty:
        raise ValueError("No data found for this stock")

    # Fix multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data[['Close', 'Volume']]

    # Tomorrow price
    data['Tomorrow'] = data['Close'].shift(-1)

    # % change
    data['Pct_Change'] = ((data['Tomorrow'] - data['Close']) / data['Close']) * 100

    data = data.dropna()

    if len(data) < 10:
        raise ValueError("Not enough data")

    # Direction
    data['Target'] = (data['Tomorrow'] > data['Close']).astype(int)

    return data


def train_model(stock):
    data = get_data(stock)

    X = data[['Close', 'Volume']]
    y = data['Target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    return model, acc, data


def predict_next_day(model, data):
    last_row = data[['Close', 'Volume']].iloc[-1]
    prediction = model.predict([last_row])[0]
    return prediction