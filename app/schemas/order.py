from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from app.models.order import OrderStatus

"""
Schemas define how clients interact with orders.
"""

class AddToCart(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: UUID
    status: OrderStatus
    total_amount: Decimal
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
