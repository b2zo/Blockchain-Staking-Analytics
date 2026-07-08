"""
Synthetic blockchain staking data generator.

This module creates realistic and internally consistent staking data for:
- networks
- validators
- delegators
- staking positions
- validator metrics
- reward transactions
- wallet metrics
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.constants import NETWORKS, TOKENS, VALIDATOR_STATUS


np.random.seed(42)

START_DATE = datetime(2024, 1, 1)
DAYS = 365
DELEGATOR_COUNT = 5000
VALIDATOR_COUNT = 100
POSITION_COUNT = 20000
REWARD_COUNT = 150000
WALLET_METRIC_COUNT = 50000


def generate_networks():
    """Generate blockchain network reference data."""

    return pd.DataFrame(
        {
            "network_name": NETWORKS,
            "symbol": TOKENS,
        }
    )


def generate_delegators(n=DELEGATOR_COUNT):
    """Generate synthetic wallet/delegator records."""

    return pd.DataFrame(
        {
            "wallet_address": [
                "0x" + "".join(np.random.choice(list("abcdef0123456789"), 40))
                for _ in range(n)
            ],
            "wallet_label": [f"Wallet_{i}" for i in range(1, n + 1)],
        }
    )


def generate_validators(n=VALIDATOR_COUNT):
    """Generate validator reference data."""

    return pd.DataFrame(
        {
            "validator_name": [f"Validator_{i}" for i in range(1, n + 1)],
            "network_id": np.random.randint(1, len(NETWORKS) + 1, n),
            "commission_rate": np.random.uniform(2, 12, n).round(2),
            "status": np.random.choice(
                VALIDATOR_STATUS,
                n,
                p=[0.9, 0.08, 0.02],
            ),
        }
    )


def generate_staking_positions(n=POSITION_COUNT):
    """
    Generate staking positions.

    Each position links one delegator wallet to one validator.
    """

    records = []

    for _ in range(n):
        records.append(
            {
                "delegator_id": np.random.randint(1, DELEGATOR_COUNT + 1),
                "validator_id": np.random.randint(1, VALIDATOR_COUNT + 1),
                "amount_staked": round(np.random.uniform(50, 25000), 6),
                "start_date": START_DATE
                + timedelta(days=int(np.random.randint(0, 90))),
                "end_date": None,
                "position_status": np.random.choice(
                    ["active", "closed"],
                    p=[0.9, 0.1],
                ),
            }
        )

    return pd.DataFrame(records)


def generate_daily_validator_metrics(days=DAYS):
    """
    Generate daily validator performance metrics.

    APR and uptime move gradually around each validator's base behaviour.
    """

    records = []

    for validator_id in range(1, VALIDATOR_COUNT + 1):
        base_apr = np.random.uniform(5, 12)
        base_uptime = np.random.uniform(97, 100)

        for day in range(days):
            metric_date = START_DATE + timedelta(days=day)

            # APR changes gradually with small noise.
            apr = base_apr + np.random.normal(0, 0.35)

            # Uptime is mostly stable and high.
            uptime = base_uptime + np.random.normal(0, 0.5)

            records.append(
                {
                    "validator_id": validator_id,
                    "metric_date": metric_date,
                    "apr": round(max(apr, 0), 4),
                    "uptime": round(min(max(uptime, 0), 100), 2),
                    "voting_power": round(np.random.uniform(100000, 5000000), 6),
                    "total_delegated": round(
                        np.random.uniform(500000, 50000000),
                        6,
                    ),
                }
            )

    return pd.DataFrame(records)


def generate_reward_transactions(
    positions: pd.DataFrame,
    validator_metrics: pd.DataFrame,
    n=REWARD_COUNT,
):
    """
    Generate reward transactions from existing positions and validator APR.

    This keeps rewards consistent with the staking positions loaded later
    into PostgreSQL.

    Reward formula:
        reward = amount_staked * APR / 365
    """

    records = []

    # Add position_id based on DataFrame row order.
    positions = positions.reset_index(drop=True).copy()
    positions["position_id"] = positions.index + 1
    
    # Ensure lookup keys have consistent data types.
    validator_metrics = validator_metrics.copy()
    validator_metrics["validator_id"] = validator_metrics["validator_id"].astype(int)
    validator_metrics["metric_date"] = pd.to_datetime(
        validator_metrics["metric_date"]
    ).dt.date

    # Build fast lookup for validator APR by validator/date.
    metrics_lookup = validator_metrics.set_index(
        ["validator_id", "metric_date"]
    )["apr"]

    for _ in range(n):
        position = positions.sample(1).iloc[0]

        reward_date = (START_DATE + timedelta(days=int(np.random.randint(0, DAYS)))).date()

        apr = metrics_lookup.loc[
            (int(position["validator_id"]), reward_date)
        ]

        reward_amount = (
            float(position["amount_staked"])
            * (apr / 100)
            / 365
        )

        # Add small noise to simulate network/reward timing variance.
        reward_amount *= np.random.uniform(0.95, 1.05)

        records.append(
            {
                "position_id": int(position["position_id"]),
                "reward_amount": round(reward_amount, 8),
                "reward_date": reward_date,
                "reward_token": np.random.choice(TOKENS),
            }
        )

    return pd.DataFrame(records)


def generate_daily_wallet_metrics(
    positions: pd.DataFrame,
    rewards: pd.DataFrame,
    n=WALLET_METRIC_COUNT,
):
    """
    Generate wallet-level daily metrics.

    Portfolio value is linked to each wallet's total staked amount
    plus accumulated rewards.
    """

    records = []

    positions = positions.reset_index(drop=True).copy()
    positions["position_id"] = positions.index + 1

    # Pre-compute wallet stake totals.
    wallet_stake = (
        positions.groupby("delegator_id")["amount_staked"]
        .sum()
        .to_dict()
    )

    # Link rewards back to delegators.
    rewards_with_wallets = rewards.merge(
        positions[["position_id", "delegator_id"]],
        on="position_id",
        how="left",
    )

    wallet_rewards = (
        rewards_with_wallets.groupby("delegator_id")["reward_amount"]
        .sum()
        .to_dict()
    )

    for _ in range(n):
        delegator_id = np.random.randint(1, DELEGATOR_COUNT + 1)
        metric_date = START_DATE + timedelta(
            days=int(np.random.randint(0, DAYS))
        )

        total_staked = wallet_stake.get(delegator_id, 0)
        total_rewards = wallet_rewards.get(delegator_id, 0)

        # Portfolio value is now based on real staking exposure.
        portfolio_value = total_staked + total_rewards

        # Add small market-value movement.
        portfolio_value *= np.random.uniform(0.95, 1.10)

        daily_rewards = portfolio_value * np.random.uniform(0.00005, 0.0004)

        active_positions = positions[
            positions["delegator_id"] == delegator_id
        ].shape[0]

        records.append(
            {
                "delegator_id": delegator_id,
                "metric_date": metric_date,
                "portfolio_value": round(portfolio_value, 6),
                "daily_rewards": round(daily_rewards, 8),
                "active_positions": active_positions,
            }
        )

    return pd.DataFrame(records).drop_duplicates(
        subset=["delegator_id", "metric_date"]
    )