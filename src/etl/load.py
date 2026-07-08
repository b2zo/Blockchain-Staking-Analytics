"""
Load module.

Loads transformed data into PostgreSQL using either append or
incremental insert logic.
"""

import pandas as pd

from src.database.db_connection import get_engine
from src.monitoring.logger import logger


def load_dataframe(df: pd.DataFrame, table_name: str) -> None:
    """Append a DataFrame into a PostgreSQL table."""

    try:
        engine = get_engine()

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000,
        )

        logger.info("%s rows loaded into %s.", len(df), table_name)
        print(f"✓ {table_name} loaded: {len(df)} rows")
        
    except Exception:
        logger.exception(
            "Failed loading table %s.",
            table_name,
        )
        raise


def incremental_load(
    df: pd.DataFrame,
    table_name: str,
    key_columns: list[str],
) -> None:
    """
    Insert only new rows into a PostgreSQL table.

    Existing rows are detected using one or more business key columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to load.

    table_name : str
        Target database table.

    key_columns : list[str]
        Columns used to identify existing records.
    """
    try:
        engine = get_engine()

        if df.empty:
            logger.info("No rows provided for %s.", table_name)
            print(f"✓ {table_name}: no rows to load")
            return

        # Read existing business keys from the target table.
        existing_keys = pd.read_sql(
            f"SELECT {', '.join(key_columns)} FROM {table_name}",
            engine,
        )

        # If the table is empty, load everything.
        if existing_keys.empty:
            load_dataframe(df, table_name)
            return
        
        # Work on copies so we do not mutate the original dataframe.
        incoming_keys = df[key_columns].copy()
        existing_keys = existing_keys.copy()

        # Ensure key columns have matching data types before comparison.
        for column in key_columns:
            if "date" in column.lower() or "time" in column.lower():
                incoming_keys[column] = pd.to_datetime(incoming_keys[column]).dt.date
                existing_keys[column] = pd.to_datetime(existing_keys[column]).dt.date
            else:
                incoming_keys[column] = incoming_keys[column].astype(str)
                existing_keys[column] = existing_keys[column].astype(str)

        # Compare only the key columns.
        merged_keys = incoming_keys.merge(
            existing_keys,
            on=key_columns,
            how="left",
            indicator=True,
        )

        # Use the original dataframe rows, not the converted copy.
        new_rows = df.reset_index(drop=True).loc[
            merged_keys["_merge"].values == "left_only"
        ]

        # Insert only new records.
        if new_rows.empty:
            logger.info("No new rows found for %s.", table_name)
            print(f"✓ {table_name}: no new rows")
            return

        load_dataframe(new_rows, table_name)
        
        logger.info(
            "%s new rows inserted into %s.",
            len(new_rows),
            table_name,
        )
        
        print(f"✓ {table_name}: {len(new_rows)} new rows inserted")
        
    except Exception as error:
         logger.exception(
            "Incremental load failed for table %s.",
            table_name,
        )
         raise