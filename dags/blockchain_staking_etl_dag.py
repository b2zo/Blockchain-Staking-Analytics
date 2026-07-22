"""
Airflow DAG for Blockchain Staking Analytics ETL.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.setup_database import setup_database
from src.etl.pipeline import (
     load_reference_data,
     load_staking_data,
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

    reference_data_task = PythonOperator(
    task_id="load_reference_data",
    python_callable=load_reference_data,
)

    staking_data_task = PythonOperator(
    task_id="load_staking_data",
    python_callable=load_staking_data,
    )

    quality_checks_task = PythonOperator(
    task_id="run_data_quality_checks",
    python_callable=run_quality_checks,
    )   

    setup_database_task >> reference_data_task >> staking_data_task >> quality_checks_task