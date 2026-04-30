from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import BOOLEAN
from sqlalchemy import UUID as DB_UUID
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class User(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(DB_UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
