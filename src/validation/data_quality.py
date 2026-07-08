"""
Data quality module for the Blockchain Staking Analytics ETL pipeline.

This module runs validation checks after data has been loaded into
PostgreSQL. The goal is to identify missing records, invalid values,
or broken business rules.
"""

import pandas as pd
from src.database.db_connection import get_engine


def run_quality_checks():
    """
    Run SQL-based data quality checks against PostgreSQL tables.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the name and result of each quality check.
    """

    # Create/reuse the database connection.
    engine = get_engine()

    # Dictionary of checks.
    # Each key is the check name, each value is the SQL query to run.
    checks = {
        # Row count checks.
        "networks_row_count": """
            SELECT COUNT(*) AS result
            FROM networks
        """,
        "delegators_row_count": """
            SELECT COUNT(*) AS result
            FROM delegators
        """,
        "validators_row_count": """
            SELECT COUNT(*) AS result
            FROM validators
        """,
        "staking_positions_row_count": """
            SELECT COUNT(*) AS result
            FROM staking_positions
        """,
        "reward_transactions_row_count": """
            SELECT COUNT(*) AS result
            FROM reward_transactions
        """,
        "daily_validator_metrics_row_count": """
            SELECT COUNT(*) AS result
            FROM daily_validator_metrics
        """,
        "daily_wallet_metrics_row_count": """
            SELECT COUNT(*) AS result
            FROM daily_wallet_metrics
        """,

        # Business rule checks.
        "negative_stake_amounts": """
            SELECT COUNT(*) AS result
            FROM staking_positions
            WHERE amount_staked <= 0
        """,
        "negative_reward_amounts": """
            SELECT COUNT(*) AS result
            FROM reward_transactions
            WHERE reward_amount < 0
        """,
        "invalid_validator_uptime": """
            SELECT COUNT(*) AS result
            FROM daily_validator_metrics
            WHERE uptime < 0 OR uptime > 100
        """,
        "invalid_validator_apr": """
            SELECT COUNT(*) AS result
            FROM daily_validator_metrics
            WHERE apr < 0
        """,
        "missing_wallet_addresses": """
            SELECT COUNT(*) AS result
            FROM delegators
            WHERE wallet_address IS NULL
               OR wallet_address = ''
        """,
    }

    results = []

    # Execute each SQL check and collect the result.
    for check_name, query in checks.items():
        result_df = pd.read_sql(query, engine)
        result_value = result_df.loc[0, "result"]

        results.append(
            {
                "check_name": check_name,
                "result": result_value,
            }
        )

    # Convert results into a clean DataFrame for reporting.
    results_df = pd.DataFrame(results)

    print("\nData Quality Check Results")
    print(results_df)

    return results_df