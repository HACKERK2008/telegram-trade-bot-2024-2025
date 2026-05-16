# utils/data_cleaner.py

import pandas as pd
import numpy as np

def remove_nulls(df: pd.DataFrame, fill_value=None) -> pd.DataFrame:
    """
    Remove or fill null/missing values in the DataFrame.

    Args:
        df (pd.DataFrame): Input data.
        fill_value (any, optional): Value to fill nulls with. 
                                    If None, drops rows with any nulls.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    return df.dropna() if fill_value is None else df.fillna(fill_value)


def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Normalize a numeric column to [0, 1] using min-max scaling.

    Args:
        df (pd.DataFrame): Input data.
        column (str): Name of the column to normalize.

    Returns:
        pd.DataFrame: Updated DataFrame with normalized column.
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' not found or not numeric.")

    col_min = df[column].min()
    col_max = df[column].max()
    df[column] = 0.0 if col_min == col_max else (df[column] - col_min) / (col_max - col_min)
    return df


def convert_to_datetime(df: pd.DataFrame, column: str, format: str = None) -> pd.DataFrame:
    """
    Convert a column to datetime, with invalid values coerced to NaT.

    Args:
        df (pd.DataFrame): Input data.
        column (str): Column to convert.
        format (str, optional): Optional datetime format.

    Returns:
        pd.DataFrame: DataFrame with the column converted to datetime.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    df[column] = pd.to_datetime(df[column], format=format, errors='coerce')
    return df


def filter_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Filter out outliers in a column using the IQR method.

    Args:
        df (pd.DataFrame): Input data.
        column (str): Column to filter for outliers.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' not found or not numeric.")

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
