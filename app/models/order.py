from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Numeric
from uuid import UUID
from decimal import Decimal
import enum

from app.models.base import Base, UUIDMixin, TimestampMixin

"""
Orders represent a checkout session.

Important rules:
- Belongs to a tenant
- Belongs to a user
- Price snapshot is stored (never recomputed)
"""

class OrderStatus(enum.Enum):
    CART = "cart"
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    # Tenant isolation (MANDATORY)
    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # User who placed the order
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Order state machine
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.CART,
        nullable=False,
    )

    # Total price snapshot (sum of order items)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False,
    )

    # Relationship to items
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
