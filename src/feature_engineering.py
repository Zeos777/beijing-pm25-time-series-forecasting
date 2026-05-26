"""Feature engineering helpers for the Beijing PM2.5 project."""

from __future__ import annotations

def create_lag_features(df, target_col="pollution", lags=(1, 2, 3)):
    """Create lagged features for the target column."""
    result = df.copy()
    for lag in lags:
        result[f"{target_col}_Lag{lag}"] = result[target_col].shift(lag)
    return result


def split_train_test_by_time(df, train_start, train_end, test_start, test_end):
    """Split a DataFrame into train and test sets using datetime ranges."""
    if "datetime" not in df.columns:
        raise KeyError("datetime column is required for time-based splitting")

    train_mask = (df["datetime"] >= train_start) & (df["datetime"] <= train_end)
    test_mask = (df["datetime"] >= test_start) & (df["datetime"] <= test_end)

    train_df = df.loc[train_mask].copy()
    test_df = df.loc[test_mask].copy()
    return train_df, test_df


def select_model_frame(df, features, target):
    """Keep only the rows needed for modeling and drop missing values."""
    columns = list(features) + [target]
    return df.dropna(subset=columns).copy()
