"""Modelo que representa una temporada de una serie."""

from __future__ import annotations

from src.extensions import db


class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "seasons"

    # COLUMNAS DEFINIDAS (ARREGLADO)
    id = db.Column(db.Integer, primary_key=True)  # CLAVE PRIMARIA
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)  # Número de temporada
    episodes_count = db.Column(db.Integer, nullable=False)  # Total de episodios

    # Restricción única por (series_id, number)
    __table_args__ = (
        db.UniqueConstraint('series_id', 'number', name='uq_series_season'),
    )

    # RELACIÓN CONFIGURADA (ARREGLADO)
    series = db.relationship("Series", back_populates="seasons")

    def to_dict(self) -> dict:
        """Serializa la temporada en un diccionario."""
        return {
            "id": self.id,
            "series_id": self.series_id,
            "number": self.number,
            "episodes_count": self.episodes_count,
        }