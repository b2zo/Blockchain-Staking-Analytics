"""
Database connection module.

Creates a reusable SQLAlchemy engine for connecting to PostgreSQL.
"""

from sqlalchemy import create_engine
from config import DB_CONFIG


# Build PostgreSQL connection URL from environment variables.
DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:"
    f"{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)

# Create SQLAlchemy engine.
# pool_pre_ping=True helps avoid stale database connections.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)


def get_engine():
    """
    Return the shared SQLAlchemy database engine.
    """

    return engine