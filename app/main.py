from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import router
from app.core.config import settings

app = FastAPI(title="Transaction Webhook Service")

# Create database tables on start, development only
if settings.ENVIRONMENT == "development":
    Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "HEALTHY"}
