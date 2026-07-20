from fastapi import FastAPI
from sqlalchemy import text
from app.routers.users import router as users_router
from app.routers.links import router as links_router
from app.database.database import Base, engine
from app.models.user import User
from app.models import link
from app.routers.auth import router as auth_router
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.link import Link

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartLink AI",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(links_router)

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
@app.get("/{short_code}")
def redirect_url(short_code: str):

    db: Session = SessionLocal()

    try:
        # Find the link
        link = db.query(Link).filter(
            Link.short_code == short_code
        ).first()

        if not link:
            return {
                "message": "Short URL not found"
            }

        # Increase click count
        link.clicks += 1

        db.commit()

        # Redirect
        return RedirectResponse(
            url=link.original_url,
            status_code=307
        )

    finally:
        db.close()