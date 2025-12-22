from fastapi import FastAPI
from app.core.database import Base, engine

app = FastAPI(title="Transaction Webhook Service")

# Create database tables on start (not ideal for production)
Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "HEALTHY"}
