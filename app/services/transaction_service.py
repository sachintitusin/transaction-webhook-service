from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate
from app.models.transaction import Transaction
from app.repositories.transaction_repo import TransactionRepository
from app.workers.transaction_worker import process_transaction


class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepository(db)
        self.db = db

    def ingest_transaction(
        self,
        payload: TransactionCreate,
        background_tasks: BackgroundTasks
    ):
        tx = Transaction(
            transaction_id=payload.transaction_id,
            source_account=payload.source_account,
            destination_account=payload.destination_account,
            amount=payload.amount,
            currency=payload.currency,
        )

        # 1. Save the transaction to DB, default status is RECEIVED
        saved_tx = self.repo.create(tx)

        # 2. Add task to background worker, process in background
        background_tasks.add_task(
            process_transaction,
            self.db,
            saved_tx.transaction_id
        )

        # Return the transaction we saved
        return saved_tx

    # Get transaction using ID
    def get_transaction(self, transaction_id: str):
        return self.repo.get_by_transaction_id(transaction_id)
