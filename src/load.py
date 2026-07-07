"""
Load module.

Loads transformed data into PostgreSQL.
"""

from db_connection import get_engine
from logger import logger


def load_dataframe(df, table_name):
    """
    Load a DataFrame into PostgreSQL.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to load.

    table_name : str
        Destination table.
    """

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

        logger.info(
            "%s rows successfully loaded into %s.",
            len(df),
            table_name,
        )

        print(f"✔ {table_name} loaded.")

    except Exception as error:
        logger.exception(
            "Failed loading table %s.",
            table_name,
        )

        raise error