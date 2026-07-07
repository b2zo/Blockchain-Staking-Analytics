/*
==========================================================
Top Validators by Total Rewards
==========================================================
*/

SELECT
    v.validator_name,
    SUM(rt.reward_amount) AS total_rewards,
    RANK() OVER (
        ORDER BY SUM(rt.reward_amount) DESC
    ) AS reward_rank
FROM reward_transactions rt
JOIN staking_positions sp
    ON rt.position_id = sp.position_id
JOIN validators v
    ON sp.validator_id = v.validator_id
GROUP BY v.validator_name
ORDER BY total_rewards DESC;

/*
==========================================================
Wallet Concentration Risk
==========================================================
*/

WITH wallet_totals AS (

SELECT

delegator_id,

SUM(amount_staked) total_staked

FROM staking_positions

GROUP BY delegator_id

)

SELECT

sp.delegator_id,

sp.validator_id,

sp.amount_staked,

ROUND(

100 * sp.amount_staked / wt.total_staked,

2

) exposure_pct

FROM staking_positions sp

JOIN wallet_totals wt

ON sp.delegator_id = wt.delegator_id;

/*
==========================================================
30-Day Rolling APR
==========================================================
*/

SELECT

validator_id,

metric_date,

apr,

AVG(apr) OVER(

PARTITION BY validator_id

ORDER BY metric_date

ROWS BETWEEN 29 PRECEDING AND CURRENT ROW

) rolling_apr

FROM daily_validator_metrics;