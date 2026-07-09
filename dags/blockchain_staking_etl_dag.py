"""
Airflow DAG for Blockchain Staking Analytics ETL.

This DAG orchestrates the full ETL pipeline:
1. Set up database schema
2. Run staking analytics ETL
3. Run data quality checks
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.setup_database import setup_database
from src.main import main


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

    run_etl_task = PythonOperator(
        task_id="run_staking_etl",
        python_callable=main,
    )

    setup_database_task >> run_etl_task