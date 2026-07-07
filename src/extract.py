import pandas as pd
import numpy as np


def generate_networks():

    return pd.DataFrame({

        "network_name": [
            "Ethereum",
            "Solana",
            "Cosmos",
            "Polkadot",
            "Cardano"
        ],

        "symbol": [
            "ETH",
            "SOL",
            "ATOM",
            "DOT",
            "ADA"
        ]

    })


def generate_validators(n=50):

    np.random.seed(42)

    return pd.DataFrame({

        "validator_name":
            [f"Validator_{i}" for i in range(1, n + 1)],

        "network_id":
            np.random.randint(1, 6, n),

        "commission_rate":
            np.random.uniform(2, 12, n).round(2),

        "status":
            np.random.choice(
                ["active", "inactive", "jailed"],
                n,
                p=[0.9, 0.08, 0.02]
            )

    })