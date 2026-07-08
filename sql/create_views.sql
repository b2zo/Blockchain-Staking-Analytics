-- ============================================================
-- Blockchain Staking Analytics
-- Analytical SQL Views
-- ============================================================

DROP VIEW IF EXISTS vw_wallet_portfolio_summary CASCADE;
DROP VIEW IF EXISTS vw_validator_performance CASCADE;
DROP VIEW IF EXISTS vw_reward_trends CASCADE;
DROP VIEW IF EXISTS vw_concentration_risk CASCADE;

CREATE VIEW vw_wallet_portfolio_summary AS
SELECT
    d.delegator_id,
    d.wallet_address,
    COUNT(sp.position_id) AS total_positions,
    SUM(sp.amount_staked) AS total_staked,
    SUM(rt.reward_amount) AS total_rewards
FROM delegators d
LEFT JOIN staking_positions sp
    ON d.delegator_id = sp.delegator_id
LEFT JOIN reward_transactions rt
    ON sp.position_id = rt.position_id
GROUP BY
    d.delegator_id,
    d.wallet_address;

CREATE VIEW vw_validator_performance AS
SELECT
    v.validator_id,
    v.validator_name,
    n.network_name,
    v.commission_rate,
    v.status,
    AVG(dvm.apr) AS avg_apr,
    AVG(dvm.uptime) AS avg_uptime,
    AVG(dvm.voting_power) AS avg_voting_power,
    AVG(dvm.total_delegated) AS avg_total_delegated
FROM validators v
JOIN networks n
    ON v.network_id = n.network_id
LEFT JOIN daily_validator_metrics dvm
    ON v.validator_id = dvm.validator_id
GROUP BY
    v.validator_id,
    v.validator_name,
    n.network_name,
    v.commission_rate,
    v.status;

CREATE VIEW vw_reward_trends AS
SELECT
    rt.reward_date,
    n.network_name,
    v.validator_name,
    SUM(rt.reward_amount) AS total_daily_rewards,
    COUNT(rt.reward_id) AS reward_transactions
FROM reward_transactions rt
JOIN staking_positions sp
    ON rt.position_id = sp.position_id
JOIN validators v
    ON sp.validator_id = v.validator_id
JOIN networks n
    ON v.network_id = n.network_id
GROUP BY
    rt.reward_date,
    n.network_name,
    v.validator_name;

CREATE VIEW vw_concentration_risk AS
SELECT
    d.delegator_id,
    d.wallet_address,
    v.validator_name,
    n.network_name,
    sp.amount_staked,
    SUM(sp.amount_staked) OVER (
        PARTITION BY d.delegator_id
    ) AS wallet_total_staked,
    ROUND(
        sp.amount_staked / NULLIF(
            SUM(sp.amount_staked) OVER (
                PARTITION BY d.delegator_id
            ), 0
        ) * 100,
        2
    ) AS validator_exposure_pct
FROM staking_positions sp
JOIN delegators d
    ON sp.delegator_id = d.delegator_id
JOIN validators v
    ON sp.validator_id = v.validator_id
JOIN networks n
    ON v.network_id = n.network_id;