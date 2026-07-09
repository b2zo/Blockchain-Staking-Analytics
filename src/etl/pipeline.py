"""
Reusable ETL pipeline tasks.
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


def load_networks():
    df = transform_networks(generate_networks())
    incremental_load(df, "networks", ["network_name"])


def load_delegators():
    df = transform_delegators(generate_delegators())
    incremental_load(df, "delegators", ["wallet_address"])


def load_validators():
    df = transform_validators(generate_validators())
    incremental_load(df, "validators", ["validator_name"])


def load_positions():
    df = transform_staking_positions(generate_staking_positions())
    incremental_load(
        df,
        "staking_positions",
        ["delegator_id", "validator_id", "amount_staked", "start_date"],
    )


def load_validator_metrics():
    df = transform_daily_validator_metrics(
        generate_daily_validator_metrics()
    )

    incremental_load(
        df,
        "daily_validator_metrics",
        ["validator_id", "metric_date"],
    )


def load_rewards():
    positions = transform_staking_positions(generate_staking_positions())

    metrics = transform_daily_validator_metrics(
        generate_daily_validator_metrics()
    )

    rewards = transform_reward_transactions(
        generate_reward_transactions(
            positions,
            metrics,
        )
    )

    incremental_load(
        rewards,
        "reward_transactions",
        ["position_id", "reward_date", "reward_amount"],
    )


def load_wallet_metrics():
    positions = transform_staking_positions(generate_staking_positions())

    metrics = transform_daily_validator_metrics(
        generate_daily_validator_metrics()
    )

    rewards = transform_reward_transactions(
        generate_reward_transactions(
            positions,
            metrics,
        )
    )

    wallet = transform_daily_wallet_metrics(
        generate_daily_wallet_metrics(
            positions,
            rewards,
        )
    )

    incremental_load(
        wallet,
        "daily_wallet_metrics",
        ["delegator_id", "metric_date"],
    )