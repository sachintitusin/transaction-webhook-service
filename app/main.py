from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import router

app = FastAPI(title="Transaction Webhook Service")

# Create database tables on start (not ideal for production)
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "HEALTHY"}
