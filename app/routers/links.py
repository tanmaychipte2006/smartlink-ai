from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.link import Link
from app.schemas.link import (
    LinkCreate,
    LinkResponse,
    LinkList
)
from app.utils.generator import generate_short_code
from app.auth.oauth2 import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/links",
    tags=["Links"]
)


@router.post("/shorten", response_model=LinkResponse)
def shorten_url(
    link: LinkCreate,
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find current user
    current_user = db.query(User).filter(
        User.email == email
    ).first()

    # Generate random short code
    short_code = generate_short_code()

    # Create database object
    new_link = Link(
        original_url=str(link.original_url),
        short_code=short_code,
        owner_id=current_user.id
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link
@router.get("/my-links", response_model=list[LinkList])
def get_my_links(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user = db.query(User).filter(
        User.email == email
    ).first()

    links = db.query(Link).filter(
        Link.owner_id == current_user.id
    ).all()

    return links
@router.delete("/{link_id}")
def delete_link(
    link_id: int,
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user = db.query(User).filter(
        User.email == email
    ).first()

    link = db.query(Link).filter(
        Link.id == link_id,
        Link.owner_id == current_user.id
    ).first()

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Link not found"
        )

    db.delete(link)
    db.commit()

    return {
        "message": "Link deleted successfully"
    }