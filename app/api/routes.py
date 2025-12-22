from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter()

@router.post("/v1/webhooks/transactions", status_code=202)
def ingest_webhook(
    payload: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    service.ingest_transaction(payload, background_tasks)
    return {"status": "ACCEPTED"}


@router.get("/v1/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService(db)
    tx = service.get_transaction(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
