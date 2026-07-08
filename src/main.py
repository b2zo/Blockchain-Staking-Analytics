"""
Main ETL entry point for the Blockchain Staking Analytics project.

This script generates synthetic blockchain staking data, transforms it,
loads it into PostgreSQL, and runs basic data quality checks.
"""
from src.database.setup_database import setup_database

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
from src.validation.data_quality import run_quality_checks
from src.monitoring.logger import logger


def main():
    """Run the full ETL pipeline."""
    
    try:
        logger.info("ETL Pipeline Started")
        print("Starting Blockchain Staking Analytics ETL...")
        logger.info("Setting up database schema.")
        setup_database()

        # Generate, transform, and load network reference data.
        networks = transform_networks(generate_networks())
        incremental_load(networks, "networks", ["network_name"])

        # Generate, transform, and load wallet/delegator data.
        delegators = transform_delegators(generate_delegators())
        incremental_load(delegators, "delegators", ["wallet_address"])

        # Generate, transform, and load validator data.
        validators = transform_validators(generate_validators())
        incremental_load(validators, "validators", ["validator_name"])

        # Generate, transform, and load staking position data.
        positions = transform_staking_positions(generate_staking_positions())
        incremental_load(positions, "staking_positions", ["delegator_id", "validator_id", "amount_staked", "start_date"],)

        # Generate, transform, and load validator daily metrics.
        validator_metrics = transform_daily_validator_metrics(
            generate_daily_validator_metrics()
        )
        incremental_load(validator_metrics, "daily_validator_metrics", ["validator_id", "metric_date"],)

        # Generate, transform, and load staking reward transactions.
        rewards = transform_reward_transactions(
            generate_reward_transactions(
                positions,
                validator_metrics,
            )
        )
        incremental_load(rewards, "reward_transactions", ["position_id", "reward_date", "reward_amount"],)

        # Generate, transform, and load wallet daily metrics.
        wallet_metrics = transform_daily_wallet_metrics(
            generate_daily_wallet_metrics(
                positions,
                rewards,
            )
        )
        incremental_load(wallet_metrics, "daily_wallet_metrics", ["delegator_id", "metric_date"],)

        # Run quality checks after all tables have been loaded.
        logger.info("Running data quality checks.")
        print("Running data quality checks...")
        run_quality_checks()

        logger.info("ETL Pipeline Finished Successfully")
        
        print("ETL Finished Successfully")

    except Exception as error:

        logger.exception(
        "Pipeline execution failed: %s",
        error
        )

        print(f"\nPipeline failed: {error}")

if __name__ == "__main__":
    main()