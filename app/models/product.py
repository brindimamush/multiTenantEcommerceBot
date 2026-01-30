from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Product(Base):
    """
    Docstring for Product

    Product that belongs to a tenant.

    All product access Must be filtered by tenant_id
    """

    __tablename__ = "products"

    # Tenant isolation column (CRITICAL)
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    # Product fields
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Use Numeric for money (To avoid float bugs)
    price = Column(Numeric(10, 2), nullable=False)

    # Inventory and visibility
    in_stock = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)