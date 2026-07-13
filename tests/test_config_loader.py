"""
Tests for the YAML configuration loader.
"""

from src.config_loader import load_config


def test_config_contains_required_sections() -> None:
    """Confirm that the main configuration sections exist."""

    config = load_config()

    assert "pipeline" in config
    assert "data_generation" in config


def test_generation_counts_are_positive() -> None:
    """Ensure configured record counts are positive integers."""

    config = load_config()
    generation_config = config["data_generation"]

    required_counts = [
        "delegator_count",
        "validator_count",
        "position_count",
        "reward_count",
        "wallet_metric_count",
    ]

    for setting in required_counts:
        assert isinstance(generation_config[setting], int)
        assert generation_config[setting] > 0