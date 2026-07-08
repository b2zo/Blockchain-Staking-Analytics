"""
==========================================================
Blockchain Staking Analytics

Transformation Module

This module contains all transformation logic used by the
ETL pipeline before loading data into PostgreSQL.

Author: Babacar Ba
==========================================================
"""

import pandas as pd


def transform_networks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardise network data.

    Parameters
    ----------
    df : DataFrame
        Raw network dataframe.

    Returns
    -------
    DataFrame
        Clean dataframe.
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces
    df["network_name"] = df["network_name"].str.strip()

    # Standardise symbols
    df["symbol"] = df["symbol"].str.upper()

    return df


def transform_delegators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean wallet information.
    """

    # Remove duplicated wallet addresses
    df = df.drop_duplicates(subset="wallet_address")

    # Ensure wallet addresses are lowercase
    df["wallet_address"] = df["wallet_address"].str.lower()

    return df


def transform_validators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate validator information.
    """

    # Keep commission within expected range
    df["commission_rate"] = df["commission_rate"].clip(0, 100)

    # Remove duplicated validator names
    df = df.drop_duplicates(subset="validator_name")

    return df


def transform_staking_positions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean staking position records.
    """

    # Remove impossible stake amounts
    df = df[df["amount_staked"] > 0]

    # Ensure active positions have no end date
    df.loc[
        df["position_status"] == "active",
        "end_date"
    ] = None

    return df


def transform_reward_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate staking rewards.
    """

    # Remove negative rewards
    df = df[df["reward_amount"] >= 0]

    return df


def transform_daily_validator_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean validator performance metrics.
    """

    # Ensure uptime remains realistic
    df["uptime"] = df["uptime"].clip(0, 100)

    # APR cannot be negative
    df["apr"] = df["apr"].clip(lower=0)

    return df


def transform_daily_wallet_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean wallet metric records.
    """

    # Portfolio values cannot be negative
    df["portfolio_value"] = df["portfolio_value"].clip(lower=0)

    # Rewards cannot be negative
    df["daily_rewards"] = df["daily_rewards"].clip(lower=0)

    return df