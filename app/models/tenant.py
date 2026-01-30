from sqlalchemy import Column, String, Boolean
from app.models.base import Base

class Tenant(Base):

    """
    Docstring for Tenant

    Represents a company / store using the platform.

    This is the heart of multitenancy.
    Every business entity links back to this table.
    """
    __tablename__ = "tenants"

    # public name of the store
    name = Column(String(255), nullable=False)

    #unique slug used in URLs or internal resolution
    slug = Column(String(100), unique=True, nullable=False)

    # Telegram bot token specific to this tenant
    telegram_bot_token = Column(String, nullable=False)

    # Branding configuration (white-label support)
    primary_color = Column(String(7), default="#000000")
    secondary_color = Column(String(7), default="#FFFFFF")

    #path or URL to upload logo
    logo_url = Column(String, nullable=True)

    # Soft-disable tenant without deleting data
    is_active = Column(Boolean, default=True)