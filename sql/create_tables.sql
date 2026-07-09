-- ============================================================
-- Blockchain Staking Analytics
-- PostgreSQL Database Schema
-- ============================================================

DROP TABLE IF EXISTS reward_transactions CASCADE;
DROP TABLE IF EXISTS staking_positions CASCADE;
DROP TABLE IF EXISTS daily_wallet_metrics CASCADE;
DROP TABLE IF EXISTS daily_validator_metrics CASCADE;
DROP TABLE IF EXISTS validators CASCADE;
DROP TABLE IF EXISTS delegators CASCADE;
DROP TABLE IF EXISTS networks CASCADE;

-- ============================================================
-- Networks
-- ============================================================

CREATE TABLE networks (
    network_id SERIAL PRIMARY KEY,
    network_name VARCHAR(100) NOT NULL UNIQUE,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Delegators / Wallets
-- ============================================================

CREATE TABLE delegators (
    delegator_id SERIAL PRIMARY KEY,
    wallet_address VARCHAR(120) NOT NULL UNIQUE,
    wallet_label VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Validators
-- ============================================================

CREATE TABLE validators (
    validator_id SERIAL PRIMARY KEY,
    validator_name VARCHAR(150) NOT NULL,
    network_id INT NOT NULL,
    commission_rate NUMERIC(5,2) NOT NULL CHECK (commission_rate >= 0 AND commission_rate <= 100),
    status VARCHAR(30) NOT NULL CHECK (status IN ('active', 'inactive', 'jailed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_validators_network
        FOREIGN KEY (network_id)
        REFERENCES networks(network_id)
);

-- ============================================================
-- Staking Positions
-- ============================================================

CREATE TABLE staking_positions (
    position_id SERIAL PRIMARY KEY,
    delegator_id INT NOT NULL,
    validator_id INT NOT NULL,
    amount_staked NUMERIC(20,6) NOT NULL CHECK (amount_staked > 0),
    start_date DATE NOT NULL,
    end_date DATE,
    position_status VARCHAR(30) NOT NULL CHECK (position_status IN ('active', 'closed')),

    CONSTRAINT fk_positions_delegator
        FOREIGN KEY (delegator_id)
        REFERENCES delegators(delegator_id),

    CONSTRAINT fk_positions_validator
        FOREIGN KEY (validator_id)
        REFERENCES validators(validator_id),

    CONSTRAINT chk_position_dates
        CHECK (end_date IS NULL OR end_date >= start_date)
);

-- ============================================================
-- Reward Transactions
-- ============================================================

CREATE TABLE reward_transactions (
    reward_id SERIAL PRIMARY KEY,
    position_id INT NOT NULL,
    reward_amount NUMERIC(20,8) NOT NULL CHECK (reward_amount >= 0),
    reward_date DATE NOT NULL,
    reward_token VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rewards_position
        FOREIGN KEY (position_id)
        REFERENCES staking_positions(position_id)
);

-- ============================================================
-- Daily Validator Metrics
-- ============================================================

CREATE TABLE daily_validator_metrics (
    metric_id SERIAL PRIMARY KEY,
    validator_id INT NOT NULL,
    metric_date DATE NOT NULL,
    apr NUMERIC(8,4) NOT NULL CHECK (apr >= 0),
    uptime NUMERIC(5,2) NOT NULL CHECK (uptime >= 0 AND uptime <= 100),
    voting_power NUMERIC(20,6) NOT NULL CHECK (voting_power >= 0),
    total_delegated NUMERIC(20,6) NOT NULL CHECK (total_delegated >= 0),

    CONSTRAINT fk_validator_metrics_validator
        FOREIGN KEY (validator_id)
        REFERENCES validators(validator_id),

    CONSTRAINT uq_validator_metric_date
        UNIQUE (validator_id, metric_date)
);

-- ============================================================
-- Daily Wallet Metrics
-- ============================================================

CREATE TABLE daily_wallet_metrics (
    metric_id SERIAL PRIMARY KEY,
    delegator_id INT NOT NULL,
    metric_date DATE NOT NULL,
    portfolio_value NUMERIC(20,6) NOT NULL CHECK (portfolio_value >= 0),
    daily_rewards NUMERIC(20,8) NOT NULL CHECK (daily_rewards >= 0),
    active_positions INT NOT NULL CHECK (active_positions >= 0),

    CONSTRAINT fk_wallet_metrics_delegator
        FOREIGN KEY (delegator_id)
        REFERENCES delegators(delegator_id),

    CONSTRAINT uq_wallet_metric_date
        UNIQUE (delegator_id, metric_date)
);

-- ============================================================
-- ETL Run Monitoring
-- ============================================================

CREATE TABLE etl_run_log (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(30) NOT NULL,
    rows_loaded INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX idx_validators_network_id
ON validators(network_id);

CREATE INDEX idx_positions_delegator_id
ON staking_positions(delegator_id);

CREATE INDEX idx_positions_validator_id
ON staking_positions(validator_id);

CREATE INDEX idx_positions_status
ON staking_positions(position_status);

CREATE INDEX idx_rewards_position_id
ON reward_transactions(position_id);

CREATE INDEX idx_rewards_date
ON reward_transactions(reward_date);

CREATE INDEX idx_validator_metrics_date
ON daily_validator_metrics(metric_date);

CREATE INDEX idx_wallet_metrics_date
ON daily_wallet_metrics(metric_date);

-- ============================================================
-- End of Schema
-- ============================================================