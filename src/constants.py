"""
Project-wide constants.
"""

# Required database tables
REQUIRED_TABLES = [
    "networks",
    "delegators",
    "validators",
    "staking_positions",
    "reward_transactions",
    "daily_validator_metrics",
    "daily_wallet_metrics",
]

NETWORKS = [
    "Ethereum",
    "Solana",
    "Cosmos",
    "Polkadot",
    "Cardano",
]

TOKENS = [
    "ETH",
    "SOL",
    "ATOM",
    "DOT",
    "ADA",
]

VALIDATOR_STATUS = [
    "active",
    "inactive",
    "jailed",
]