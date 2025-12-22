from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_transaction_id(self, transaction_id: str):
        return (
            self.db.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )

    def create(self, tx: Transaction):
        try:
            self.db.add(tx)
            self.db.commit()
            self.db.refresh(tx)
            return tx
        except IntegrityError:
            # Idempotency hit (duplicate transaction_id)
            self.db.rollback()
            return self.get_by_transaction_id(tx.transaction_id)
