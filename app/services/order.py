from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from decimal import Decimal

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product

"""
Order service enforces:
- Tenant safety
- Order lifecycle
- Price integrity
"""

async def get_or_create_cart(
    db: AsyncSession,
    tenant_id: UUID,
    user_id: UUID,
) -> Order:
    """
    Ensures a user has only ONE active cart.
    """

    stmt = select(Order).where(
        Order.tenant_id == tenant_id,
        Order.user_id == user_id,
        Order.status == OrderStatus.CART,
    )

    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if cart:
        return cart

    cart = Order(
        tenant_id=tenant_id,
        user_id=user_id,
        status=OrderStatus.CART,
    )

    db.add(cart)
    await db.commit()
    await db.refresh(cart)

    return cart


async def add_item_to_cart(
    db: AsyncSession,
    tenant_id: UUID,
    user_id: UUID,
    product_id: UUID,
    quantity: int,
) -> Order:
    """
    Adds or updates an item in the cart.
    """

    cart = await get_or_create_cart(db, tenant_id, user_id)

    # Fetch product safely
    stmt = select(Product).where(
        Product.id == product_id,
        Product.tenant_id == tenant_id,
        Product.is_active == True,
    )

    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise ValueError("Product not available")

    # Check if item already exists
    for item in cart.items:
        if item.product_id == product.id:
            item.quantity += quantity
            break
    else:
        cart.items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
            )
        )

    # Recalculate total
    cart.total_amount = sum(
        item.unit_price * item.quantity
        for item in cart.items
    )

    await db.commit()
    await db.refresh(cart)

    return cart


async def checkout_cart(
    db: AsyncSession,
    tenant_id: UUID,
    user_id: UUID,
) -> Order:
    """
    Locks cart and moves it to PENDING_PAYMENT.
    """

    stmt = select(Order).where(
        Order.tenant_id == tenant_id,
        Order.user_id == user_id,
        Order.status == OrderStatus.CART,
    )

    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    cart.status = OrderStatus.PENDING_PAYMENT

    await db.commit()
    await db.refresh(cart)

    return cart
