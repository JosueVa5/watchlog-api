"""Modelo principal para las peliculas."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(120), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)
    release_year: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    def __repr__(self) -> str:
        return f"<Movie id={self.id} title={self.title}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_year": self.release_year,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }