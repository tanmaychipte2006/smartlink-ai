from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.link import Link
from app.schemas.link import (
    LinkCreate,
    LinkResponse,
    LinkList,
    LinkUpdate,
    LinkStats
)
from app.qr.generator import generate_qr
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
    short_url = f"http://192.168.1.105:8000/{short_code}"

    qr_path = generate_qr(
    short_url,
    short_code
     )

    # Create database object
    new_link = Link(
    original_url=str(link.original_url),
    short_code=short_code,
    owner_id=current_user.id,
    qr_code=qr_path
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
@router.put("/{link_id}", response_model=LinkResponse)
def update_link(
    link_id: int,
    updated_link: LinkUpdate,
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

    link.original_url = str(updated_link.original_url)

    db.commit()
    db.refresh(link)

    return link
@router.get("/stats", response_model=LinkStats)
def get_stats(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user = db.query(User).filter(
        User.email == email
    ).first()

    links = db.query(Link).filter(
        Link.owner_id == current_user.id
    ).all()

    total_links = len(links)

    total_clicks = sum(link.clicks for link in links)

    most_clicked = None

    if links:
        most_clicked = max(
            links,
            key=lambda x: x.clicks
        ).short_code

    return {
        "total_links": total_links,
        "total_clicks": total_clicks,
        "most_clicked_link": most_clicked
    }