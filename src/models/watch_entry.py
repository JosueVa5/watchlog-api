"""Modelo puente que guarda el progreso del usuario."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    # COLUMNAS DEFINIDAS
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'movie' o 'series'
    content_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, watching, completed
    
    # Columnas de progreso
    current_season = db.Column(db.Integer, default=1)
    current_episode = db.Column(db.Integer, default=0)
    watched_episodes = db.Column(db.Integer, default=0)
    total_episodes = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # RELACIONES
    user = db.relationship("User", back_populates="watch_entries")

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        if self.total_episodes == 0:
            return 0.0
        
        if self.status == 'completed':
            return 100.0
            
        percentage = (self.watched_episodes / self.total_episodes) * 100
        return min(percentage, 100.0)  # No más del 100%

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        self.status = 'completed'
        if self.content_type == 'series':
            self.watched_episodes = self.total_episodes
        else:  # movie
            self.watched_episodes = 1
            self.total_episodes = 1
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
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
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }