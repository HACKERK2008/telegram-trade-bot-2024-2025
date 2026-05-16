# tests/test_option_zone_labeler.py

import pandas as pd
from analyzer.option_zone_labeler import label_option_zones

def test_option_zone_labeling():
    # Sample dummy option chain
    data = {
        "strike": [25000, 25100, 25200, 25300, 25400],
        "call_ltp": [300, 200, 150, 80, 40],
        "put_ltp":  [40, 80, 150, 200, 300],
    }
    spot_price = 25210.0  # Nearest ATM = 25200

    df = pd.DataFrame(data)
    labeled_df = label_option_zones(df, spot_price)

    assert labeled_df.loc[labeled_df["strike"] == 25200, "call_zone"].values[0] == "ATM"
    assert labeled_df.loc[labeled_df["strike"] == 25200, "put_zone"].values[0] == "ATM"

    assert labeled_df.loc[labeled_df["strike"] == 25000, "call_zone"].values[0] == "ITM"
    assert labeled_df.loc[labeled_df["strike"] == 25400, "call_zone"].values[0] == "OTM"

    assert labeled_df.loc[labeled_df["strike"] == 25000, "put_zone"].values[0] == "OTM"
    assert labeled_df.loc[labeled_df["strike"] == 25400, "put_zone"].values[0] == "ITM"

    print("✅ option_zone_labeler test passed.")

if __name__ == "__main__":
    test_option_zone_labeling()
