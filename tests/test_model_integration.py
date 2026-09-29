"""Tests de integración modelo + datos locales (sin red)."""

import os
import warnings

import joblib
import pandas as pd
import pytest

from utils.model_loader import predict_binary, predict_probabilities

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "models", "baseline_model.joblib")
LIVE_PATH = os.path.join(ROOT, "data", "processed", "live_demo.parquet")


@pytest.fixture(scope="module")
def artifact():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return joblib.load(MODEL_PATH)


@pytest.fixture(scope="module")
def live_df():
    df = pd.read_parquet(LIVE_PATH)
    if "machineID" in df.columns:
        df = df.rename(columns={"machineID": "machine_id"})
    return df


def test_artifact_has_required_keys(artifact):
    assert {"model", "feature_cols", "model_type", "decision_threshold"} <= set(artifact)
    assert len(artifact["feature_cols"]) == 46
    assert 0 <= artifact["decision_threshold"] <= 1


def test_live_data_has_model_features(artifact, live_df):
    missing = set(artifact["feature_cols"]) - set(live_df.columns)
    assert not missing, f"Faltan features en live_demo.parquet: {missing}"
    assert live_df["machine_id"].nunique() == 100


def test_probabilities_in_range(artifact, live_df):
    sample = live_df.head(500)
    probs = predict_probabilities(artifact["model"], artifact["feature_cols"], sample)
    assert len(probs) == len(sample)
    assert probs.between(0, 1).all()


def test_predict_probabilities_raises_on_missing_features(artifact, live_df):
    incomplete = live_df.head(10).drop(columns=[artifact["feature_cols"][0]])
    with pytest.raises(ValueError, match="Faltan features"):
        predict_probabilities(artifact["model"], artifact["feature_cols"], incomplete)


def test_predict_binary_rejects_invalid_threshold(artifact, live_df):
    with pytest.raises(ValueError, match="umbral"):
        predict_binary(artifact["model"], artifact["feature_cols"], live_df.head(5), 1.5)


def test_predict_binary_respects_threshold(artifact, live_df):
    sample = live_df.head(500)
    args = (artifact["model"], artifact["feature_cols"], sample)
    assert predict_binary(*args, threshold=0.0).eq(1).all()
    assert predict_binary(*args, threshold=1.0).sum() <= (
        predict_probabilities(*args) >= 1.0
    ).sum()
