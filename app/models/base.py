from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Base(DeclarativeBase):
    """
    Docstring for Base
    
    Base class for all SQLALchemy models.

    - Centralizes common columns
    - Enforces consistency across tables
    - Makes migrations predictable

    """

    # primary key used by all tables
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Automatically updated when row changes
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )