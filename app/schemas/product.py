from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

"""
Schemas define the API contract.

They insure:
- Validation at the boundary
- No ORM leakage to clients

"""

class ProductCreate(BaseModel):
    """
    Docstring for ProductCreate
    Payload for creating a product (admin only).
    """

    name:str = Field(...,min_length=1, max_length=255)
    description:str | None = None

    # Decimal is mandatory for money
    price: Decimal = Field(...,gt=0)

    in_stock: bool = True
    is_active: bool = True

class ProductUpdate(BaseModel):
    """
    Docstring for ProductUpdate

    Payload for updating a product.
    All fields optional to support Ptch semantics.

    """

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    in_stock: bool | None = None
    is_active: bool | None = None

class ProductResponse(BaseModel):
    """
    Docstring for ProductResponse
    Product data returned to clients.
    """
    id: UUID
    name: str
    description: str | None
    price: Decimal
    in_stock : bool
    is_active: bool

    class Config:
        from_attributes = True