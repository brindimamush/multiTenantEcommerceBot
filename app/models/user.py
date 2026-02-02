from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from .base import UUIDMixin, TimestampMixin, Base
import uuid

class User(Base, UUIDMixin, TimestampMixin):
    """
    Docstring for User

    Represents a Telegram user inside a specific tenant.

    Important:
    - Same Telegram user can exist in multiple tenants
    - Therefore: tenant_id is mandatory
    """

    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Tenant isolation column (CRITICAL)
    tenant_id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    # Telegram-provided unique user ID
    telegram_user_id: Mapped[str] = mapped_column(String, nullable=False)

    # Display name from Telegram
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)

    # Role-based access (admin vs customer)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)