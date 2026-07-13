"""
Unit tests for ETL transformation functions.
"""

import pandas as pd

from src.etl.transform import (
    transform_networks,
    transform_delegators,
    transform_validators,
    transform_staking_positions,
    transform_reward_transactions,
    transform_daily_validator_metrics,
    transform_daily_wallet_metrics,
)


def test_network_symbols_are_uppercase() -> None:
    """Network symbols should be standardized to uppercase."""

    source = pd.DataFrame(
        {
            "network_name": [" Ethereum "],
            "symbol": ["eth"],
        }
    )

    result = transform_networks(source)

    assert result.loc[0, "network_name"] == "Ethereum"
    assert result.loc[0, "symbol"] == "ETH"


def test_duplicate_wallets_are_removed() -> None:
    """Duplicate wallet addresses should only appear once."""

    source = pd.DataFrame(
        {
            "wallet_address": ["0xABC", "0xABC"],
            "wallet_label": ["Wallet_1", "Wallet_1_Copy"],
        }
    )

    result = transform_delegators(source)

    assert len(result) == 1
    assert result.iloc[0]["wallet_address"] == "0xabc"


def test_validator_commission_is_clipped() -> None:
    """Commission rates must remain between zero and 100."""

    source = pd.DataFrame(
        {
            "validator_name": ["Validator_1", "Validator_2"],
            "network_id": [1, 1],
            "commission_rate": [-5.0, 120.0],
            "status": ["active", "inactive"],
        }
    )

    result = transform_validators(source)

    assert result["commission_rate"].tolist() == [0.0, 100.0]


def test_invalid_staking_amounts_are_removed() -> None:
    """Zero and negative staking positions should be rejected."""

    source = pd.DataFrame(
        {
            "delegator_id": [1, 2, 3],
            "validator_id": [1, 1, 2],
            "amount_staked": [100.0, 0.0, -50.0],
            "start_date": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-03"]
            ),
            "end_date": [None, None, None],
            "position_status": ["active", "active", "closed"],
        }
    )

    result = transform_staking_positions(source)

    assert len(result) == 1
    assert result.iloc[0]["amount_staked"] == 100.0


def test_negative_rewards_are_removed() -> None:
    """Negative staking rewards should not pass transformation."""

    source = pd.DataFrame(
        {
            "position_id": [1, 2],
            "reward_amount": [1.25, -0.50],
            "reward_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "reward_token": ["ETH", "ETH"],
        }
    )

    result = transform_reward_transactions(source)

    assert len(result) == 1
    assert result.iloc[0]["reward_amount"] == 1.25


def test_validator_metrics_are_clipped() -> None:
    """APR and uptime should stay within accepted boundaries."""

    source = pd.DataFrame(
        {
            "validator_id": [1],
            "metric_date": pd.to_datetime(["2024-01-01"]),
            "apr": [-2.0],
            "uptime": [104.0],
            "voting_power": [1000.0],
            "total_delegated": [5000.0],
        }
    )

    result = transform_daily_validator_metrics(source)

    assert result.iloc[0]["apr"] == 0.0
    assert result.iloc[0]["uptime"] == 100.0


def test_wallet_values_are_non_negative() -> None:
    """Portfolio values and rewards should not remain negative."""

    source = pd.DataFrame(
        {
            "delegator_id": [1],
            "metric_date": pd.to_datetime(["2024-01-01"]),
            "portfolio_value": [-100.0],
            "daily_rewards": [-2.0],
            "active_positions": [1],
        }
    )

    result = transform_daily_wallet_metrics(source)

    assert result.iloc[0]["portfolio_value"] == 0.0
    assert result.iloc[0]["daily_rewards"] == 0.0