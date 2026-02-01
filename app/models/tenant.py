from sqlalchemy import String, Boolean
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Tenant(Base):

    """
    Docstring for Tenant

    Represents a company / store using the platform.

    This is the heart of multitenancy.
    Every business entity links back to this table.
    """
    __tablename__ = "tenants"

    # public name of the store
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    #unique slug used in URLs or internal resolution
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Telegram bot token specific to this tenant
    telegram_bot_token: Mapped[str] = mapped_column(String, nullable=False)

    # Branding configuration (white-label support)
    primary_color: Mapped[str] = mapped_column(String(7), default="#000000")
    secondary_color: Mapped[str] = mapped_column(String(7), default="#FFFFFF")

    #path or URL to upload logo
    logo_url : Mapped[str | None] = mapped_column(nullable=True)

    # Soft-disable tenant without deleting data
    is_active: Mapped[str] = mapped_column(Boolean, default=True)