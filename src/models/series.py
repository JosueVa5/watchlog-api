"""Modelo para series disponibles en el catalogo."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

class Series(db.Model):
    """Representa una serie cargada por los usuarios."""

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    total_seasons: Mapped[int] = mapped_column(default=1)
    synopsis: Mapped[str] = mapped_column(db.Text, nullable=True)
    genres: Mapped[str] = mapped_column(db.String(200), nullable=True)
    image_url: Mapped[str] = mapped_column(db.String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relaciones
    seasons = relationship("Season", back_populates="series", cascade="all, delete-orphan")
    watch_entries = relationship("WatchEntry", back_populates="series", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Series id={self.id} title={self.title}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        data = {
            "id": self.id,
            "title": self.title,
            "total_seasons": self.total_seasons,
            "synopsis": self.synopsis,
            "genres": self.genres,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        
        if include_seasons:
            data["seasons"] = [season.to_dict() for season in self.seasons]
            
        return data

    def get_total_episodes(self) -> int:
        """Calcula el total de episodios de todas las temporadas."""
        return sum(season.episodes_count for season in self.seasons)