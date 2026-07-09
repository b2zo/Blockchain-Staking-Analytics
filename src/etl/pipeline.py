"""
Reusable ETL pipeline tasks for Airflow and local execution.
"""

from src.etl.extract import (
    generate_networks,
    generate_delegators,
    generate_validators,
    generate_staking_positions,
    generate_reward_transactions,
    generate_daily_validator_metrics,
    generate_daily_wallet_metrics,
)
from src.etl.transform import (
    transform_networks,
    transform_delegators,
    transform_validators,
    transform_staking_positions,
    transform_reward_transactions,
    transform_daily_validator_metrics,
    transform_daily_wallet_metrics,
)
from src.etl.load import incremental_load


def load_reference_data() -> None:
    """Load networks, delegators, and validators."""

    incremental_load(
        transform_networks(generate_networks()),
        "networks",
        ["network_name"],
    )

    incremental_load(
        transform_delegators(generate_delegators()),
        "delegators",
        ["wallet_address"],
    )

    incremental_load(
        transform_validators(generate_validators()),
        "validators",
        ["validator_name"],
    )


def load_staking_data() -> None:
    """Load staking positions, validator metrics, rewards, and wallet metrics."""

    positions = transform_staking_positions(generate_staking_positions())

    validator_metrics = transform_daily_validator_metrics(
        generate_daily_validator_metrics()
    )

    rewards = transform_reward_transactions(
        generate_reward_transactions(
            positions,
            validator_metrics,
        )
    )

    wallet_metrics = transform_daily_wallet_metrics(
        generate_daily_wallet_metrics(
            positions,
            rewards,
        )
    )

    incremental_load(
        positions,
        "staking_positions",
        ["delegator_id", "validator_id", "amount_staked", "start_date"],
    )

    incremental_load(
        validator_metrics,
        "daily_validator_metrics",
        ["validator_id", "metric_date"],
    )

    incremental_load(
        rewards,
        "reward_transactions",
        ["position_id", "reward_date", "reward_amount"],
    )

    incremental_load(
        wallet_metrics,
        "daily_wallet_metrics",
        ["delegator_id", "metric_date"],
    )