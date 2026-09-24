"""Tests de compute_risk_from_model usando el modelo y datos locales."""

import warnings

import pytest

from utils.data_loader import compute_risk_from_model, load_live_demo_data

VALID_LEVELS = {"Estable", "Moderado", "Crítico"}
VALID_PRIORITIES = {"Intervenir", "Inspeccionar", "Monitorear", "Ninguna"}


@pytest.fixture(scope="module")
def risk_outputs():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        live_df, source = load_live_demo_data(prefer_local=True)
        return live_df, source, compute_risk_from_model(live_df, prefer_local_model=True)


def test_local_source_is_used(risk_outputs):
    _, source, _ = risk_outputs
    assert source.startswith("Local")


def test_one_row_per_machine(risk_outputs):
    live_df, _, (_, df_risk, _, _) = risk_outputs
    assert len(df_risk) == live_df["machine_id"].nunique()
    assert df_risk["machine_id"].is_unique


def test_risk_levels_match_score_thresholds(risk_outputs):
    _, _, (_, df_risk, _, _) = risk_outputs
    assert set(df_risk["risk_level"]) <= VALID_LEVELS
    assert set(df_risk["priority"]) <= VALID_PRIORITIES
    assert df_risk["risk_score"].between(0, 100).all()
    assert (df_risk.loc[df_risk["risk_score"] < 30, "risk_level"] == "Estable").all()
    assert (df_risk.loc[df_risk["risk_score"] >= 60, "risk_level"] == "Crítico").all()


def test_machine_ids_are_strings_in_all_frames(risk_outputs):
    _, _, frames = risk_outputs
    for df in frames:
        assert df["machine_id"].map(type).eq(str).all()


def test_telemetry_uses_names_expected_by_components(risk_outputs):
    _, _, (_, _, df_telemetry, _) = risk_outputs
    assert {"timestamp", "machine_id", "temperature", "vibration", "pressure"} <= set(
        df_telemetry.columns
    )
