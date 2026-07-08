"""
Database setup module.

Executes SQL scripts required to initialise the PostgreSQL database:
- create tables
- create analytical views
"""

from pathlib import Path


from sqlalchemy import text
from sqlalchemy import inspect

from src.database.db_connection import get_engine
from src.monitoring.logger import logger

from src.constants import REQUIRED_TABLES
required_tables = set(REQUIRED_TABLES)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SQL_FILES = [
    PROJECT_ROOT / "sql" / "create_tables.sql",
    PROJECT_ROOT / "sql" / "create_views.sql",
    PROJECT_ROOT / "sql" / "advanced_analytics.sql",
]


def run_sql_file(file_path: Path) -> None:
    """
    Execute a SQL file against the configured PostgreSQL database.

    Parameters
    ----------
    file_path : Path
        Path to the SQL file.
    """

    engine = get_engine()

    logger.info("Running SQL file: %s", file_path)

    sql = file_path.read_text(encoding="utf-8")

    with engine.begin() as connection:
        connection.execute(text(sql))

    logger.info("Successfully executed SQL file: %s", file_path.name)
    
    
def database_initialized() -> bool:
    """
    Check whether the database schema already exists.

    Returns
    -------
    bool
        True if the required tables already exist.
    """

    engine = get_engine()

    inspector = inspect(engine)

    existing_tables = set(inspector.get_table_names())

    return required_tables.issubset(existing_tables)


def setup_database():
    """
    Initialise the PostgreSQL database only once.
    """

    if database_initialized():
        logger.info("Database schema already exists. Skipping setup.")
        print("✓ Database already initialized.")
        return

    logger.info("Creating database schema...")

    for sql_file in SQL_FILES:
        run_sql_file(sql_file)

    logger.info("Database setup completed.")
    print("✓ Database initialized successfully.")