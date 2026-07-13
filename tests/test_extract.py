"""
Tests for synthetic blockchain data generation.
"""

from src.etl.extract import (
    generate_networks,
    generate_delegators,
    generate_validators,
    generate_staking_positions,
)


def test_network_generator_returns_expected_columns() -> None:
    """Networks should contain the required database fields."""

    result = generate_networks()

    assert set(result.columns) == {"network_name", "symbol"}
    assert not result.empty


def test_delegator_generator_respects_requested_size() -> None:
    """Delegator generator should return the requested number of rows."""

    result = generate_delegators(n=10)

    assert len(result) == 10
    assert result["wallet_address"].is_unique


def test_validator_generator_uses_valid_statuses() -> None:
    """Validator statuses must match supported business values."""

    result = generate_validators(n=20)

    allowed_statuses = {"active", "inactive", "jailed"}

    assert set(result["status"]).issubset(allowed_statuses)


def test_staking_positions_have_positive_amounts() -> None:
    """All generated positions should contain positive stake amounts."""

    result = generate_staking_positions(n=25)

    assert len(result) == 25
    assert (result["amount_staked"] > 0).all()