from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_tenant_db
from app.core.context import current_tenant_id, current_user_id
from app.schemas.order import AddToCart, OrderResponse
from app.services.order import add_item_to_cart, checkout_cart

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/cart/items", response_model=OrderResponse)
async def add_to_cart(
    payload: AddToCart,
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Adds product to the user's cart.
    """

    try:
        return await add_item_to_cart(
            db=db,
            tenant_id=current_tenant_id.get(),
            user_id=current_user_id.get(),
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout", response_model=OrderResponse)
async def checkout(
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Locks cart and prepares for payment.
    """

    try:
        return await checkout_cart(
            db=db,
            tenant_id=current_tenant_id.get(),
            user_id=current_user_id.get(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
