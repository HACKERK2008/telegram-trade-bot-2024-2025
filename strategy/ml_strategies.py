# strategy/ml_strategies.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MLTrendPredictor:
    """
    Machine learning-based trend classifier using Random Forest.
    Learns from past OHLC data to predict 'up' or 'down' next candle.
    """

    def __init__(self, model=None, test_size: float = 0.2):
        self.model = model or RandomForestClassifier(n_estimators=100, random_state=42)
        self.test_size = test_size
        self.trained = False
        self.accuracy = None

    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["return"] = df["close"].pct_change()
        df["sma_5"] = df["close"].rolling(5).mean()
        df["sma_10"] = df["close"].rolling(10).mean()
        df["momentum"] = df["close"] - df["close"].shift(5)
        df["volatility"] = df["return"].rolling(5).std()
        df.dropna(inplace=True)
        return df

    def _label_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df["label"] = df["close"].shift(-1) > df["close"]
        df["label"] = df["label"].astype(int)  # 1 for UP, 0 for DOWN
        df.dropna(inplace=True)
        return df

    def prepare_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        df = self._create_features(df)
        df = self._label_data(df)
        features = df[["return", "sma_5", "sma_10", "momentum", "volatility"]]
        labels = df["label"]
        return features, labels

    def train(self, df: pd.DataFrame) -> float:
        X, y = self.prepare_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        self.trained = True
        print(f"✅ ML model trained | Accuracy: {self.accuracy:.2%}")
        return self.accuracy

    def predict_next(self, df: pd.DataFrame) -> str:
        if not self.trained:
            self.train(df)

        X, _ = self.prepare_data(df)
        last_row = X.iloc[[-1]]
        prediction = self.model.predict(last_row)[0]
        return "up" if prediction == 1 else "down"

    def describe(self):
        return f"🤖 MLTrendPredictor | Accuracy: {self.accuracy:.2%}" if self.trained else "🤖 MLTrendPredictor (untrained)"
