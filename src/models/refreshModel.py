from datetime import datetime,timezone
from uuid import uuid4, UUID

from sqlalchemy import String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.baseModel import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    replaced_by_token_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),   # supports IPv6
        nullable=True,
        index=True
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True
    )

    device: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    os: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    browser: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    country: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    city: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    user = relationship("User", back_populates="refresh_tokens")

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at

    def is_active(self) -> bool:
        return not self.revoked and not self.is_expired()