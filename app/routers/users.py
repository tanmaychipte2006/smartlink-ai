from fastapi import APIRouter, Depends

from app.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def current_user(
    email: str = Depends(get_current_user)
):

    return {
        "message": "Protected Route ✅",
        "email": email
    }