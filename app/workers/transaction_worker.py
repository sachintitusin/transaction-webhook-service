import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus


def process_transaction(db: Session, transaction_id: str):
    # 1. Query the DB for given transaction id
    tx = (
        db.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id)
        .first()
    )

    # 2. Skip processing if transaction not found, or already processed
    if not tx or tx.status == TransactionStatus.PROCESSED:
        return

    tx.status = TransactionStatus.PROCESSING
    db.commit()

    # Simulate external API call, wait 30s
    time.sleep(30)

    # Change transaction status and processed_at timestamp
    tx.status = TransactionStatus.PROCESSED
    tx.processed_at = datetime.utcnow()
    db.commit()
