"""Modelo puente que guarda el progreso del usuario."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    content_type: Mapped[str] = mapped_column(db.String(20), nullable=False)  # 'movie' o 'series'
    content_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(db.String(20), default='pending')  # pending, watching, completed
    
    # Columnas de progreso
    current_season: Mapped[int] = mapped_column(default=1)
    current_episode: Mapped[int] = mapped_column(default=0)
    watched_episodes: Mapped[int] = mapped_column(default=0)
    total_episodes: Mapped[int] = mapped_column(default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # RELACIÓN SIMPLIFICADA - solo con User
    user = relationship("User", back_populates="watch_entries")

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        if self.total_episodes == 0:
            return 0.0
        
        if self.status == 'completed':
            return 100.0
            
        percentage = (self.watched_episodes / self.total_episodes) * 100
        return min(round(percentage, 2), 100.0)

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        self.status = 'completed'
        if self.content_type == 'series':
            self.watched_episodes = self.total_episodes
            self.current_episode = self.total_episodes
        else:  # movie
            self.watched_episodes = 1
            self.total_episodes = 1
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "status": self.status,
            "current_season": self.current_season,
            "current_episode": self.current_episode,
            "watched_episodes": self.watched_episodes,
            "total_episodes": self.total_episodes,
            "percentage_watched": self.percentage_watched(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }