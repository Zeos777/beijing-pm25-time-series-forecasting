"""Model fitting and prediction helpers."""

from __future__ import annotations

import statsmodels.api as sm


def fit_ols(train_df, features, target):
    """Fit an OLS model with an intercept term."""
    X_train = train_df[list(features)]
    y_train = train_df[target]
    X_train_const = sm.add_constant(X_train, has_constant="add")
    model = sm.OLS(y_train, X_train_const).fit()
    return model


def predict_ols(model, test_df, features):
    """Predict with an OLS model using the same feature columns as training."""
    X_test = test_df[list(features)]
    X_test_const = sm.add_constant(X_test, has_constant="add")

    exog_names = model.model.exog_names
    X_test_const = X_test_const.reindex(columns=exog_names)
    return model.predict(X_test_const)
