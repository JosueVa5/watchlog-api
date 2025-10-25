"""Modelo para usuarios que usan la plataforma."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

class User(db.Model):
    """Representa a un usuario."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    # Relación con WatchEntry
    watch_entries = relationship("WatchEntry", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }