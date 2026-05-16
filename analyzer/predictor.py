# analyzer/predictor.py

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go

def train_predictor_model(df):
    """
    Trains an XGBoost model on pre-analyzed data.
    Required columns: ['rsi', 'macd', 'atr', 'return_1', 'bb_width', 'close']
    """
    df = df.copy()
    df.dropna(inplace=True)

    # Create binary target
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)

    features = ['rsi', 'macd', 'atr', 'return_1', 'bb_width']
    X = df[features]
    y = df['target']

    if y.nunique() < 2:
        raise ValueError("❌ Target variable has only one class (0 or 1). Cannot train model.")

    split = int(len(df) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    return model, round(acc * 100, 2)

def predict_from_analyzed_data(df, model):
    """
    Uses a trained model and processed data to generate prediction and confidence.
    """
    latest = df.tail(1)
    features = ['rsi', 'macd', 'atr', 'return_1', 'bb_width']
    pred = model.predict(latest[features])[0]
    signal = "BUY CALL" if pred == 1 else "BUY PUT"
    return signal

def generate_confidence(model, df):
    """
    Estimate confidence based on model probability.
    """
    features = ['rsi', 'macd', 'atr', 'return_1', 'bb_width']
    latest = df.tail(1)
    proba = model.predict_proba(latest[features])[0]
    return round(max(proba) * 100, 2)

def plot_latest_candles(df, title="Price Chart"):
    fig = go.Figure(go.Candlestick(
        x=df.index, open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        name="Price"
    ))
    fig.update_layout(title=title, xaxis_rangeslider_visible=False)
    return fig

# ✅ ADD THIS FUNCTION TO CONNECT TO analyzer.py
def predict_trade(df):
    """
    Full wrapper for analyzer.py
    Returns prediction and confidence based on XGBoost model
    """
    model, acc = train_predictor_model(df)
    signal = predict_from_analyzed_data(df, model)
    confidence = generate_confidence(model, df)
    return signal, confidence
