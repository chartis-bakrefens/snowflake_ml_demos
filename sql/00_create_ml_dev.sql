-- Development home for models built in this repo; future staging ground for the model registry.
-- Run as HAT_DATASCIENCE_ANALYST (holds HAT_DATASCIENCE_DB.HAT_DATASCIENCE_CREATOR). Idempotent.
CREATE SCHEMA IF NOT EXISTS HAT_DATASCIENCE_DB.ML_DEV
    COMMENT = 'ML development: Snowpark ML models, experiments and mock_ demo tables. Synthetic data only in demos.';
