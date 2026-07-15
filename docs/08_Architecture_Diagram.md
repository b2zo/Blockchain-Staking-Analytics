# Blockchain Staking Analytics — Architecture

This project implements a containerised blockchain staking analytics platform with automated orchestration, incremental loading, monitoring, testing, and analytical reporting.

```mermaid
flowchart TD
    A[Airflow Scheduler] --> B[Database Setup Task]

    B --> C[Reference Data Pipeline]
    B --> D[Staking Data Pipeline]

    C --> C1[Generate Networks]
    C --> C2[Generate Delegators]
    C --> C3[Generate Validators]

    D --> D1[Generate Staking Positions]
    D --> D2[Generate Validator Metrics]
    D --> D3[Generate Reward Transactions]
    D --> D4[Generate Wallet Metrics]

    C1 --> E[Transform Layer]
    C2 --> E
    C3 --> E
    D1 --> E
    D2 --> E
    D3 --> E
    D4 --> E

    E --> F[Incremental Loader]
    F --> G[(PostgreSQL)]

    G --> H[Analytical SQL Views]
    G --> I[Advanced SQL Analytics]
    G --> J[ETL Run Monitoring]
    G --> K[Data Quality Checks]

    H --> L[Power BI Dashboard]
    I --> L
    J --> L
    K --> L

    M[Docker Compose] -. manages .-> A
    M -. manages .-> F
    M -. manages .-> G

    N[GitHub Actions CI] --> O[Run Pytest]
    N --> P[Build Docker Image]
```

## Data Flow

1. Airflow schedules and orchestrates the pipeline.
2. Synthetic blockchain staking datasets are generated.
3. Transformation functions clean and standardise the records.
4. Incremental loading prevents duplicate records.
5. PostgreSQL stores operational and analytical data.
6. Data quality checks validate important business rules.
7. ETL monitoring records pipeline execution status.
8. SQL views provide reporting-ready datasets.
9. Power BI consumes the analytical views.
10. GitHub Actions automatically runs tests and builds the Docker image.