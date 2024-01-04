from typing import Optional

from sqlalchemy.orm import Session

from service.learning.database.models import Artist


def get_artist(db: Session, artist_id: str) -> Optional[Artist]:
    return db.query(Artist).filter(Artist.id == artist_id).first()
