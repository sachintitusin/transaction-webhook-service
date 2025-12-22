from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionStatus
from app.models.transaction import Transaction
from app.workers.transaction_worker import process_transaction

class DummyBackgroundTasks:
    def add_task(self, *args, **kwargs):
        pass

def test_idempotent_webhook_ingestion(db_session):
    service = TransactionService(db_session)

    payload = TransactionCreate(
        transaction_id="txn_idem_1",
        source_account="acc_a",
        destination_account="acc_b",
        amount=100,
        currency="INR"
    )

    bg = DummyBackgroundTasks()

    service.ingest_transaction(payload, bg)
    service.ingest_transaction(payload, bg)
    service.ingest_transaction(payload, bg)

    rows = db_session.query(Transaction).all()

    assert len(rows) == 1
    assert rows[0].transaction_id == "txn_idem_1"

def test_processed_transaction_is_not_reprocessed(db_session):
    tx = Transaction(
        transaction_id="txn_done",
        source_account="a",
        destination_account="b",
        amount=100,
        currency="INR",
        status=TransactionStatus.PROCESSED
    )

    db_session.add(tx)
    db_session.commit()

    process_transaction(db_session, "txn_done")

    refreshed = (
        db_session.query(Transaction)
        .filter_by(transaction_id="txn_done")
        .first()
    )

    assert refreshed.status == TransactionStatus.PROCESSED


    tx = Transaction(
        transaction_id="txn_flow",
        source_account="a",
        destination_account="b",
        amount=100,
        currency="INR"
    )

    db_session.add(tx)
    db_session.commit()

    # simulate worker start
    tx.status = TransactionStatus.PROCESSING
    db_session.commit()

    # simulate worker finish
    tx.status = TransactionStatus.PROCESSED
    db_session.commit()

    refreshed = (
        db_session.query(Transaction)
        .filter_by(transaction_id="txn_flow")
        .first()
    )

    assert refreshed.status == TransactionStatus.PROCESSED
