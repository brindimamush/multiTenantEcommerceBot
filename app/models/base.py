from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4
from datetime import datetime

class Base(DeclarativeBase):
    """
    Docstring for Base
    
    Base class for all SQLALchemy models.

    - Centralizes common columns
    - Enforces consistency across tables
    - Makes migrations predictable

    """

    # primary key used by all tables
    pass

class UUIDMixin:
    """
    Provides a UUID primary key.

    Why UUID?
    - Safer for multi-tenant systems
    - No ID guessing
    - Works well across services
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        index=True,
        nullable=False,
    )


class TimestampMixin:
    """
    Adds created_at and updated_at timestamps.

    These are critical for:
    - Auditing
    - Debugging
    - Order lifecycle tracking
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )