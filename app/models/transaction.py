import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    UniqueConstraint
)
from sqlalchemy.sql import func
from app.core.database import Base


class TransactionStatus(str, enum.Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Idempotency key
    transaction_id = Column(String, nullable=False)

    source_account = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    status = Column(
        Enum(TransactionStatus),
        nullable=False,
        default=TransactionStatus.RECEIVED
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    processed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "transaction_id",
            name="uq_transaction_transaction_id"
        ),
    )
