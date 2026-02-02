from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

"""
Service layer contains all product-related business rules.

Endpoints call services.
Services talk to the database.
"""

async def create_product(
    db: AsyncSession,
    tenant_id: UUID,
    data: ProductCreate,
) -> Product:
    """
    Creates a new product for a tenant.
    """

    product = Product(
        tenant_id=tenant_id,
        name=data.name,
        description=data.description,
        price=data.price,
        in_stock=data.in_stock,
        is_active=data.is_active,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


async def list_products(
    db: AsyncSession,
    tenant_id: UUID,
    include_inactive: bool = False,
):
    """
    Lists products for a tenant.

    Non-admin users should not see inactive products.
    """

    stmt = select(Product).where(Product.tenant_id == tenant_id)

    if not include_inactive:
        stmt = stmt.where(Product.is_active == True)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_product(
    db: AsyncSession,
    tenant_id: UUID,
    product_id: UUID,
) -> Product | None:
    """
    Fetches a single product, tenant-safe.
    """

    stmt = select(Product).where(
        Product.id == product_id,
        Product.tenant_id == tenant_id,
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_product(
    db: AsyncSession,
    tenant_id: UUID,
    product_id: UUID,
    data: ProductUpdate,
) -> Product | None:
    """
    Updates product fields selectively.
    """

    product = await get_product(db, tenant_id, product_id)

    if not product:
        return None

    # Apply partial updates safely
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


async def delete_product(
    db: AsyncSession,
    tenant_id: UUID,
    product_id: UUID,
) -> bool:
    """
    Soft-delete product by deactivating it.
    """

    product = await get_product(db, tenant_id, product_id)

    if not product:
        return False

    product.is_active = False
    await db.commit()

    return True
