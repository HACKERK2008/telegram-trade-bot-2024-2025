# visualizer/chart_generator.py

import mplfinance as mpf
import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_main_price_candlestick(df: pd.DataFrame, symbol: str, save_path: str = None) -> str:
    if save_path is None:
        save_path = f"charts/{symbol}_price_chart.png"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df_plot = df.rename(columns={
        "open": "Open", "high": "High", "low": "Low",
        "close": "Close", "volume": "Volume"
    })

    mc = mpf.make_marketcolors(up='green', down='red', inherit=True)
    style = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)

    try:
        mpf.plot(
            df_plot,
            type="candle",
            volume=True,
            style=style,
            title=f"{symbol.upper()} – Price + Volume ({df.index[-1].strftime('%d %b %Y')})",
            ylabel="Price",
            ylabel_lower="Volume",
            figratio=(16, 9),
            figscale=1.2,
            savefig=save_path
        )
        print(f"✅ Price chart saved to {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Failed to plot candlestick chart: {e}")
        return None

def plot_option_chain_text_as_image(text_block: str, symbol: str, save_path: str = None) -> str:
    if save_path is None:
        save_path = f"charts/{symbol}_option_chain.png"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axis('off')
        ax.text(0.01, 1.01, text_block, fontsize=10, family='monospace',
                verticalalignment='top', transform=ax.transAxes)
        fig.tight_layout()
        fig.savefig(save_path, dpi=200)
        plt.close(fig)
        print(f"✅ Option chain chart saved to {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Failed to render option chain text image: {e}")
        return None
