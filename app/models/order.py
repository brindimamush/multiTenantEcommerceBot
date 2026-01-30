from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Order(Base):
    """
    Docstring for Order

    Represents a purchase made by a user.

    Orders are tenant-bound and immutable after payment.
    """

    __tablename__ = "orders"

    # Tenant isolation
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    # Who placed the order
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Total order value
    total_amount = Column(Numeric(10,2), nullable=False)

    # Order status lifecycle
    status = Column(
        String(50),
        default="pending" # pending, paid, cancelled, shipped
    )