from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from .base import UUIDMixin, TimestampMixin, Base

class Product(Base, UUIDMixin, TimestampMixin):
    """
    Docstring for Product

    Product that belongs to a tenant.

    All product access Must be filtered by tenant_id
    """

    __tablename__ = "products"

    # Tenant isolation column (CRITICAL)
    tenant_id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    # Product fields
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    description:Mapped[str] = mapped_column(Text ,nullable=True)

    # Use Numeric for money (To avoid float bugs)
    price:Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Inventory and visibility
    in_stock:Mapped[bool] = mapped_column(Boolean, default=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)