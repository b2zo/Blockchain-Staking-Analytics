"""
Airflow DAG for Blockchain Staking Analytics ETL.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.setup_database import setup_database
from src.etl.pipeline import (
    load_networks,
    load_delegators,
    load_validators,
    load_positions,
    load_validator_metrics,
    load_rewards,
    load_wallet_metrics,
)
from src.validation.data_quality import run_quality_checks


default_args = {
    "owner": "Babacar Ba",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="blockchain_staking_analytics_etl",
    description="Daily ETL pipeline for blockchain staking analytics",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["blockchain", "staking", "etl", "postgresql"],
) as dag:

    setup_database_task = PythonOperator(
        task_id="setup_database",
        python_callable=setup_database,
    )

    networks_task = PythonOperator(
        task_id="load_networks",
        python_callable=load_networks,
    )

    delegators_task = PythonOperator(
        task_id="load_delegators",
        python_callable=load_delegators,
    )

    validators_task = PythonOperator(
        task_id="load_validators",
        python_callable=load_validators,
    )

    positions_task = PythonOperator(
        task_id="load_staking_positions",
        python_callable=load_positions,
    )

    validator_metrics_task = PythonOperator(
        task_id="load_validator_metrics",
        python_callable=load_validator_metrics,
    )

    rewards_task = PythonOperator(
        task_id="load_rewards",
        python_callable=load_rewards,
    )

    wallet_metrics_task = PythonOperator(
        task_id="load_wallet_metrics",
        python_callable=load_wallet_metrics,
    )

    quality_checks_task = PythonOperator(
        task_id="run_data_quality_checks",
        python_callable=run_quality_checks,
    )

    setup_database_task >> [networks_task, delegators_task, validators_task]

    [delegators_task, validators_task] >> positions_task

    validators_task >> validator_metrics_task

    [positions_task, validator_metrics_task] >> rewards_task

    [positions_task, rewards_task] >> wallet_metrics_task

    [
        networks_task,
        delegators_task,
        validators_task,
        positions_task,
        validator_metrics_task,
        rewards_task,
        wallet_metrics_task,
    ] >> quality_checks_task