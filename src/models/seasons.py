"""Modelo que representa una temporada de una serie."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from src.extensions import db

class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    series_id: Mapped[int] = mapped_column(db.ForeignKey('series.id'), nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)  # Número de temporada
    episodes_count: Mapped[int] = mapped_column(nullable=False)  # Total de episodios
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    # Restricción única por (series_id, number)
    __table_args__ = (
        UniqueConstraint('series_id', 'number', name='uq_series_season'),
    )

    # Relación con Series
    series = relationship("Series", back_populates="seasons")

    def __repr__(self) -> str:
        return f"<Season id={self.id} series_id={self.series_id} number={self.number}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "series_id": self.series_id,
            "number": self.number,
            "episodes_count": self.episodes_count,
            "created_at": self.created_at.isoformat(),
        }