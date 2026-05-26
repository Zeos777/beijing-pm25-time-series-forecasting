"""Evaluation helpers for training and test metrics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.stattools import durbin_watson


def calculate_training_metrics(model):
    """Return core training metrics from a fitted statsmodels OLS model."""
    resid = model.resid
    s = np.sqrt(np.sum(resid ** 2) / model.df_resid)
    return {
        "R-squared": float(model.rsquared),
        "Adjusted R-squared": float(model.rsquared_adj),
        "S": float(s),
        "Durbin-Watson": float(durbin_watson(resid)),
    }


def calculate_test_metrics(y_true, y_pred):
    """Calculate test-set error metrics."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    errors = y_true - y_pred
    mad = np.mean(np.abs(errors))
    mse = np.mean(errors ** 2)
    rmse = np.sqrt(mse)

    nonzero_mask = y_true != 0
    if np.any(nonzero_mask):
        pct_errors = (y_true[nonzero_mask] - y_pred[nonzero_mask]) / y_true[nonzero_mask]
        mape = np.mean(np.abs(pct_errors)) * 100
        mpe = np.mean(pct_errors) * 100
    else:
        mape = np.nan
        mpe = np.nan

    return {
        "MAD": float(mad),
        "MSE": float(mse),
        "RMSE": float(rmse),
        "MAPE": float(mape),
        "MPE": float(mpe),
    }


def save_regression_summary(model, output_path):
    """Save the statsmodels summary text to a file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(model.summary().as_text(), encoding="utf-8")


def save_metrics(metrics, output_path):
    """Save metric values to CSV using pandas."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([metrics]).to_csv(output_path, index=False)
