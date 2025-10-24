"""Modelo para usuarios que usan la plataforma."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class User(db.Model):
    """Representa a un usuario (simulado mediante el header X-User-Id)."""

    __tablename__ = "users"

    # COLUMNAS DEFINIDAS
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # RELACIÓN CON WATCHENTRY
    watch_entries = db.relationship("WatchEntry", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Devuelve una representacion legible del usuario."""
        return f"<User id={self.id} name={self.name}>"

    def to_dict(self) -> dict:
        """Serializa al usuario para respuestas JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }