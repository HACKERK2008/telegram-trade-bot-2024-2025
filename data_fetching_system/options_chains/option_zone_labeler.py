# analyzer/option_zone_labeler.py

import pandas as pd

def label_option_zones(df: pd.DataFrame, spot_price: float) -> pd.DataFrame:
    """
    Labels each strike in the option chain as ITM/ATM/OTM for CALL and PUT.

    Parameters:
    - df: DataFrame with at least a 'strike' column.
    - spot_price: The live spot price of the index/stock.

    Returns:
    - DataFrame with added columns: 'call_zone', 'put_zone'
    """

    if "strike" not in df.columns:
        raise ValueError("Option chain DataFrame must contain 'strike' column.")

    # Determine the closest strike (ATM)
    df = df.copy()
    df["distance"] = abs(df["strike"] - spot_price)
    atm_strike = df.loc[df["distance"].idxmin(), "strike"]
    df.drop(columns=["distance"], inplace=True)

    def get_call_zone(strike):
        if strike == atm_strike:
            return "ATM"
        elif strike < spot_price:
            return "ITM"
        else:
            return "OTM"

    def get_put_zone(strike):
        if strike == atm_strike:
            return "ATM"
        elif strike > spot_price:
            return "ITM"
        else:
            return "OTM"

    df["call_zone"] = df["strike"].apply(get_call_zone)
    df["put_zone"] = df["strike"].apply(get_put_zone)
    df["atm_strike"] = atm_strike  # Useful for later steps

    return df
