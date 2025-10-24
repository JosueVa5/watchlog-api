"""Modelo para series disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Series(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "series"

    # COLUMNAS DEFINIDAS (ARREGLADO)
    id = db.Column(db.Integer, primary_key=True)  # CLAVE PRIMARIA
    title = db.Column(db.String(100), nullable=False)
    total_seasons = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Columnas opcionales
    synopsis = db.Column(db.Text)
    genres = db.Column(db.String(200))
    image_url = db.Column(db.String(500))

    # RELACIÓN CONFIGURADA (ARREGLADO)
    seasons = db.relationship("Season", back_populates="series", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={self.id} title={self.title}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        data = {
            "id": self.id,
            "title": self.title,
            "total_seasons": self.total_seasons,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "synopsis": self.synopsis,
            "genres": self.genres,
            "image_url": self.image_url,
        }
        
        if include_seasons and hasattr(self, 'seasons'):
            data["seasons"] = [season.to_dict() for season in self.seasons]
            
        return data