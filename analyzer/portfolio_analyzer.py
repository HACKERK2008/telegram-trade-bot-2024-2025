# analyzer/portfolio_analyzer.py

import pandas as pd
import yfinance as yf
import numpy as np

def fetch_latest_prices(symbols: list) -> dict:
    """
    Use yfinance to fetch latest close prices for given symbols.
    """
    data = yf.download(tickers=" ".join(symbols), period="1d", interval="1d", progress=False)
    closes = data['Close'].iloc[-1] if not data.empty else {}
    return closes.to_dict() if hasattr(closes, 'to_dict') else {}

def analyze_portfolio(positions: list[dict]) -> dict:
    """
    positions = [
        {'symbol': 'RELIANCE.NS', 'quantity': 10, 'avg_price': 2700},
        {'symbol': 'TCS.NS', 'quantity': 5, 'avg_price': 3300},
    ]
    """
    df = pd.DataFrame(positions)
    df['symbol'] = df['symbol'].str.upper()
    
    prices = fetch_latest_prices(df['symbol'].tolist())
    df['current_price'] = df['symbol'].map(prices)
    df['current_value'] = df['quantity'] * df['current_price']
    df['invested'] = df['quantity'] * df['avg_price']
    df['pnl'] = df['current_value'] - df['invested']
    df['pnl_pct'] = (df['pnl'] / df['invested']) * 100

    total_value = df['current_value'].sum()
    df['weight_pct'] = (df['current_value'] / total_value) * 100

    max_exposure = df['weight_pct'].max()
    max_pos = df.loc[df['weight_pct'].idxmax()]

    risk_summary = {
        'total_investment': round(df['invested'].sum(), 2),
        'total_value': round(total_value, 2),
        'total_pnl': round(df['pnl'].sum(), 2),
        'total_pnl_pct': round((df['pnl'].sum() / df['invested'].sum()) * 100, 2),
        'max_weight_symbol': max_pos['symbol'],
        'max_weight_pct': round(max_pos['weight_pct'], 2)
    }

    return {
        "holdings": df.round(2).to_dict(orient='records'),
        "summary": risk_summary
    }
