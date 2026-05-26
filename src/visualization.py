"""Matplotlib plotting helpers for the Beijing PM2.5 project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def _prepare_output_path(output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def plot_training_timeseries(train_df, output_path):
    output_path = _prepare_output_path(output_path)
    plt.figure(figsize=(12, 5))
    plt.plot(train_df["datetime"], train_df["pollution"], linewidth=0.8)
    plt.title("Training Set PM2.5 Values Over Time")
    plt.xlabel("Date")
    plt.ylabel("PM2.5")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_actual_vs_predicted(test_df, y_true, y_pred, output_path):
    output_path = _prepare_output_path(output_path)
    plt.figure(figsize=(12, 5))
    plt.plot(test_df["datetime"], y_true, label="Actual", linewidth=2)
    plt.plot(test_df["datetime"], y_pred, label="Predicted", linewidth=2)
    plt.title("Actual vs Predicted PM2.5 on Test Set")
    plt.xlabel("Date")
    plt.ylabel("PM2.5")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_prediction_errors(test_df, errors, output_path):
    output_path = _prepare_output_path(output_path)
    plt.figure(figsize=(12, 4))
    plt.plot(test_df["datetime"], errors, linewidth=1.5)
    plt.axhline(0, linestyle="--")
    plt.title("Prediction Errors on Test Set")
    plt.xlabel("Date")
    plt.ylabel("Actual - Predicted")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_residuals_vs_fitted(model, output_path):
    output_path = _prepare_output_path(output_path)
    plt.figure(figsize=(6, 5))
    plt.scatter(model.fittedvalues, model.resid, alpha=0.4, s=10)
    plt.axhline(0, linestyle="--")
    plt.title("Residuals vs Fitted Values")
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_residual_distribution(model, output_path):
    output_path = _prepare_output_path(output_path)
    plt.figure(figsize=(6, 5))
    plt.hist(model.resid, bins=50)
    plt.title("Distribution of Training Residuals")
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
