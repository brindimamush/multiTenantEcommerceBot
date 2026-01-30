from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class User(Base):
    """
    Docstring for User

    Represents a Telegram user inside a specific tenant.

    Important:
    - Same Telegram user can exist in multiple tenants
    - Therefore: tenant_id is mandatory
    """

    __tablename__ = "users"

    # Tenant isolation column (CRITICAL)
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    # Telegram-provided unique user ID
    telegram_user_id = Column(String, nullable=False)

    # Display name from Telegram
    full_name = Column(String, nullable=True)

    # Role-based access (admin vs customer)
    is_admin = Column(Boolean, default=False)