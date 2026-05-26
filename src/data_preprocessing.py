"""Basic data preprocessing helpers for the Beijing PM2.5 project."""

from __future__ import annotations

import pandas as pd


def load_raw_data(path):
    """Load the raw CSV file into a DataFrame."""
    return pd.read_csv(path)


def add_datetime(df):
    """Create a datetime column from year, month, day, and hour."""
    result = df.copy()
    result["datetime"] = pd.to_datetime(result[["year", "month", "day", "hour"]])
    return result


def sort_by_datetime(df):
    """Sort rows by datetime and reset the index."""
    if "datetime" not in df.columns:
        raise KeyError("datetime column is required before sorting")
    return df.sort_values("datetime").reset_index(drop=True)


def rename_columns(df):
    """Rename raw columns to clearer analysis names."""
    return df.rename(
        columns={
            "pm2.5": "pollution",
            "DEWP": "dew",
            "TEMP": "temp",
            "PRES": "press",
            "Iws": "wnd_spd",
            "Is": "snow",
            "Ir": "rain",
        }
    )


def handle_missing_pm25(df, strategy="fill_zero"):
    """Handle missing PM2.5 values with the first baseline strategy."""
    if strategy != "fill_zero":
        raise ValueError("Only strategy='fill_zero' is supported for now.")
    if "pollution" not in df.columns:
        raise KeyError("pollution column is required before handling missing values")
    result = df.copy()
    result["pollution"] = result["pollution"].fillna(0)
    return result
