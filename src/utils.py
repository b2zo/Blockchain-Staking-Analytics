"""
==========================================================
Blockchain Staking Analytics

Utility Functions

Common helper functions used across the ETL pipeline.

Author: Babacar Ba
==========================================================
"""

from datetime import datetime


def print_stage(stage_name: str):
    """
    Print a formatted ETL stage header.

    Parameters
    ----------
    stage_name : str
        Name of the current ETL stage.
    """

    print("\n" + "=" * 60)
    print(f"{stage_name}")
    print("=" * 60)


def current_timestamp():
    """
    Return the current timestamp.

    Returns
    -------
    str
        Current timestamp in YYYY-MM-DD HH:MM:SS format.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")