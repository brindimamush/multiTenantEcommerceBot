from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric
from uuid import UUID
from decimal import Decimal

from app.models.base import Base, UUIDMixin

"""
OrderItem stores a snapshot of product data at purchase time.

NEVER reference product price dynamically.
"""

class OrderItem(Base, UUIDMixin):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )

    product_name: Mapped[str] = mapped_column(nullable=False)

    # Price snapshot
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(nullable=False)

    order = relationship("Order", back_populates="items")
