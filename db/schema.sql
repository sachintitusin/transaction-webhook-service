CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,

    transaction_id VARCHAR NOT NULL UNIQUE,

    source_account VARCHAR NOT NULL,
    destination_account VARCHAR NOT NULL,

    amount INTEGER NOT NULL,
    currency VARCHAR NOT NULL,

    status VARCHAR NOT NULL CHECK (
        status IN ('RECEIVED', 'PROCESSING', 'PROCESSED')
    ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ NULL
);
