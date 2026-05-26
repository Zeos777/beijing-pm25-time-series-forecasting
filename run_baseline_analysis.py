"""Run the baseline PM2.5 analysis workflow from the project root."""

from pathlib import Path

from src.data_preprocessing import (
    add_datetime,
    handle_missing_pm25,
    load_raw_data,
    rename_columns,
    sort_by_datetime,
)
from src.evaluation import (
    calculate_test_metrics,
    calculate_training_metrics,
    save_metrics,
    save_regression_summary,
)
from src.feature_engineering import (
    create_lag_features,
    select_model_frame,
    split_train_test_by_time,
)
from src.modeling import fit_ols, predict_ols
from src.visualization import (
    plot_actual_vs_predicted,
    plot_prediction_errors,
    plot_residual_distribution,
    plot_residuals_vs_fitted,
    plot_training_timeseries,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "raw" / "beijing_pm25.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = BASE_DIR / "figures"

TRAIN_START = "2010-01-01 00:00:00"
TRAIN_END = "2014-12-24 23:00:00"
TEST_START = "2014-12-25 00:00:00"
TEST_END = "2014-12-31 23:00:00"

FEATURES = [
    "dew",
    "temp",
    "press",
    "wnd_spd",
    "snow",
    "rain",
    "pollution_Lag1",
    "pollution_Lag2",
    "pollution_Lag3",
]
TARGET = "pollution"


def main():
    df = load_raw_data(DATA_PATH)
    df = add_datetime(df)
    df = sort_by_datetime(df)
    df = rename_columns(df)
    df = handle_missing_pm25(df, strategy="fill_zero")
    df = create_lag_features(df, target_col=TARGET, lags=(1, 2, 3))

    train_df, test_df = split_train_test_by_time(
        df,
        train_start=TRAIN_START,
        train_end=TRAIN_END,
        test_start=TEST_START,
        test_end=TEST_END,
    )

    train_model = select_model_frame(train_df, FEATURES, TARGET)
    test_model = select_model_frame(test_df, FEATURES, TARGET)

    model = fit_ols(train_model, FEATURES, TARGET)
    y_pred = predict_ols(model, test_model, FEATURES)
    y_test = test_model[TARGET]
    errors = y_test - y_pred

    training_metrics = calculate_training_metrics(model)
    test_metrics = calculate_test_metrics(y_test, y_pred)

    save_regression_summary(model, OUTPUTS_DIR / "regression_summary.txt")
    save_metrics(test_metrics, OUTPUTS_DIR / "baseline_metrics.csv")

    plot_training_timeseries(train_df, FIGURES_DIR / "training_pollution_timeseries.png")
    plot_actual_vs_predicted(
        test_model,
        y_true=y_test,
        y_pred=y_pred,
        output_path=FIGURES_DIR / "actual_vs_predicted.png",
    )
    plot_prediction_errors(
        test_model,
        errors=errors,
        output_path=FIGURES_DIR / "prediction_errors.png",
    )
    plot_residuals_vs_fitted(
        model,
        output_path=FIGURES_DIR / "residuals_vs_fitted.png",
    )
    plot_residual_distribution(
        model,
        output_path=FIGURES_DIR / "residual_distribution.png",
    )

    print("Training metrics:")
    for key, value in training_metrics.items():
        print(f"{key}: {value:.6f}")

    print("\nTest metrics:")
    for key, value in test_metrics.items():
        print(f"{key}: {value:.6f}")

    print("\nSaved outputs:")
    print(f"- {OUTPUTS_DIR / 'regression_summary.txt'}")
    print(f"- {OUTPUTS_DIR / 'baseline_metrics.csv'}")
    print(f"- {FIGURES_DIR / 'training_pollution_timeseries.png'}")
    print(f"- {FIGURES_DIR / 'actual_vs_predicted.png'}")
    print(f"- {FIGURES_DIR / 'prediction_errors.png'}")
    print(f"- {FIGURES_DIR / 'residuals_vs_fitted.png'}")
    print(f"- {FIGURES_DIR / 'residual_distribution.png'}")


if __name__ == "__main__":
    main()
