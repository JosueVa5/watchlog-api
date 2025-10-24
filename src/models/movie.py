"""Modelo para peliculas disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Movie(db.Model):
    """Representa una pelicula cargada por los usuarios."""

    __tablename__ = "movies"

    # COLUMNAS DEFINIDAS
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    release_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Columnas opcionales
    synopsis = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duración en minutos
    image_url = db.Column(db.String(500))

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Movie id={self.id} title={self.title}>"

    def to_dict(self) -> dict:
        """Serializa la pelicula para respuestas JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_year": self.release_year,
            "synopsis": self.synopsis,
            "duration": self.duration,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }