# Transaction Webhook Processing Service

## Overview

This service handles incoming **transaction webhooks** from external payment providers (e.g., Razorpay-like systems).
The core requirement is to **acknowledge webhooks immediately** while **processing transactions asynchronously** in the background.

The design focuses on:
- Fast acknowledgment (≤ 500ms)
- Idempotency (safe retries from webhook providers)
- Correctness over scale
- Clear invariants enforced via code and tests

---

## What the Service Does

### API Endpoints

#### 1. Health Check
```
GET /
```

Returns a simple health response to verify the service is running.

---

#### 2. Webhook Ingestion
```
POST /v1/webhooks/transactions
```

Accepts transaction webhooks in the following format:

```json
{
  "transaction_id": "txn_abc123",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1500,
  "currency": "INR"
}
```

Behavior:
- Always responds with **202 Accepted**
- Responds immediately (does not wait for processing)
- Duplicate webhooks with the same `transaction_id` are handled safely

---

#### 3. Transaction Status (for testing)
```
GET /v1/transactions/{transaction_id}
```

Returns the current state of the transaction:
- `RECEIVED`
- `PROCESSING`
- `PROCESSED`

This endpoint is **read-only** and never triggers processing.

---

## Core Design Decisions

### Fast acknowledgment is mandatory
Webhook providers retry aggressively on slow or non-2xx responses.
For this reason, webhook ingestion and transaction processing are **strictly decoupled**.

The API persists the transaction first, schedules background processing, and returns `202` immediately.

---

### Idempotency is enforced at the database level
Multiple webhooks for the same transaction must not cause duplicate processing.

This is enforced using:
- A **unique constraint** on `transaction_id`
- Repository logic that safely handles duplicate inserts

---

### Background processing
Transaction processing is handled using **FastAPI BackgroundTasks**.

Important characteristics:
- The HTTP response is sent **before** background execution starts
- Processing runs after the request lifecycle completes
- The request itself is never blocked by the 30-second delay

---

### State transitions
Transactions follow a simple state machine:

```
RECEIVED → PROCESSING → PROCESSED
```

Once a transaction reaches `PROCESSED`, it is terminal and will never be processed again.

---

## Invariants

- A webhook is always acknowledged quickly
- A transaction is processed at most once
- Duplicate webhooks do not create duplicate records
- Once processed, a transaction cannot be reprocessed
- Transactions are never silently lost after acknowledgment

These invariants are enforced via database constraints, service logic, and unit tests.

---

## Testing Strategy

Tests verify:
- Idempotent webhook ingestion
- Terminal behavior of processed transactions
- Safety under retries

An isolated in-memory SQLite database is used for tests.

---

## Project Structure

```
app/
  api/
  core/
  models/
  schemas/
  repositories/
  services/
  workers/
tests/
  conftest.py
  test_invariants.py
```

---

## Running the Project

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the service
```bash
uvicorn app.main:app --reload
```

### Run tests
```bash
pytest
```

---

## Production Considerations

This implementation is production-correct in terms of data integrity and behavior, but intentionally simplified.

In a real production environment, background processing could be evolved into:
- Queue-based workers (Redis / SQS)
- Dedicated worker services
- Retry handling and dead-letter queues
- Observability (logging, metrics, tracing)

---

## Final Notes

The goal of this project is to demonstrate:
- Clear system thinking
- Explicit invariants
- Safe handling of real-world webhook behavior
- Honest engineering tradeoffs
