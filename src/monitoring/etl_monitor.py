"""
ETL monitoring utilities.

Records pipeline execution status in PostgreSQL.
"""

from datetime import datetime
from sqlalchemy import text

from src.database.db_connection import get_engine
from src.monitoring.logger import logger


def start_etl_run(pipeline_name: str) -> int:
    """Create a new ETL run record and return its run_id."""

    engine = get_engine()

    query = text(
        """
        INSERT INTO etl_run_log (
            pipeline_name,
            start_time,
            status
        )
        VALUES (
            :pipeline_name,
            :start_time,
            'RUNNING'
        )
        RETURNING run_id
        """
    )

    with engine.begin() as connection:
        run_id = connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "start_time": datetime.now(),
            },
        ).scalar_one()

    logger.info("Started ETL run %s.", run_id)

    return run_id


def finish_etl_run(
    run_id: int,
    status: str,
    rows_loaded: int = 0,
    error_message: str | None = None,
) -> None:
    """Update an ETL run record with final status."""

    engine = get_engine()

    query = text(
        """
        UPDATE etl_run_log
        SET
            end_time = :end_time,
            status = :status,
            rows_loaded = :rows_loaded,
            error_message = :error_message
        WHERE run_id = :run_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "run_id": run_id,
                "end_time": datetime.now(),
                "status": status,
                "rows_loaded": rows_loaded,
                "error_message": error_message,
            },
        )

    logger.info("Finished ETL run %s with status %s.", run_id, status)