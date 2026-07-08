validators

delegations

rewards

epochs

blocks

transactions

wallets

staking_positions

audit_logs

etl_runs


NETWORK
──────────────
network_id
network_name
symbol

        │

        │

VALIDATORS
──────────────
validator_id
validator_name
network_id
commission
status

        │

        │

STAKING_POSITIONS
────────────────────
position_id
delegator_id
validator_id
amount_staked
start_date

        │

        │

REWARD_TRANSACTIONS
────────────────────
reward_id
position_id
reward_amount
reward_date

DELEGATORS
──────────────
delegator_id
wallet_address

DAILY_VALIDATOR_METRICS
──────────────────────────
validator_id
date
apr
uptime
voting_power

DAILY_WALLET_METRICS
──────────────────────
wallet_id
date
portfolio_value
daily_rewards