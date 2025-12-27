from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.models.transaction import TransactionStatus

class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    source_account: str = Field(..., min_length=1)
    destination_account: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=1)

class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: Decimal
    currency: str
    status: TransactionStatus
    created_at: datetime
    processed_at: Optional[datetime]

    # Config is an inner configuration class for Pydantic
    class Config:
        # Returning correct JSON instead of SQLAlchemy obj
        # We do it only on responses
        orm_mode = True
