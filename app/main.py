from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import Base, engine
from app.models.user import User
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartLink AI",
    version="1.0.0"
)
app.include_router(auth_router)


@app.get("/")
def home():
    try:
        with engine.connect() as connection:
            version = connection.execute(text("SELECT version();")).scalar()

        return {
            "status": "Connected Successfully ✅",
            "database": version
        }

    except Exception as e:
        return {
            "status": "Connection Failed ❌",
            "error": str(e)
        }