"""
Unit tests for the transformation module.
"""

import pandas as pd

from src.etl.transform import transform_networks


def test_network_symbols_are_uppercase():
    """Ensure network symbols are converted to uppercase."""

    df = pd.DataFrame(
        {
            "network_name": ["Ethereum"],
            "symbol": ["eth"],
        }
    )

    result = transform_networks(df)

    assert result.loc[0, "symbol"] == "ETH"