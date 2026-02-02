from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_tenant_db
from app.core.context import (
    current_tenant_id,
    current_user_is_admin,
)
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.services.product import (
    create_product,
    list_products,
    get_product,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(
    data: ProductCreate,
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Create a product.
    Admin-only.
    """

    if not current_user_is_admin.get():
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    tenant_id = current_tenant_id.get()

    product = await create_product(
        db=db,
        tenant_id=tenant_id,
        data=data
    )

    return product


@router.get("/", response_model=list[ProductResponse])
async def list_products_endpoint(
    include_inactive: bool = Query(default=False),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    List products.

    - Customers: active products only
    - Admins: optionally include inactive
    """

    tenant_id = current_tenant_id.get()

    products = await list_products(
        db=db,
        tenant_id=tenant_id,
        include_inactive=include_inactive and current_user_is_admin.get()
    )

    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Fetch a single product.
    """

    tenant_id = current_tenant_id.get()

    product = await get_product(
        db=db,
        tenant_id=tenant_id,
        product_id=product_id
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Update product.
    Admin-only.
    """

    if not current_user_is_admin.get():
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    tenant_id = current_tenant_id.get()

    product = await update_product(
        db=db,
        tenant_id=tenant_id,
        product_id=product_id,
        data=data
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/{product_id}")
async def delete_product_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Soft-delete product.
    Admin-only.
    """

    if not current_user_is_admin.get():
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    tenant_id = current_tenant_id.get()

    deleted = await delete_product(
        db=db,
        tenant_id=tenant_id,
        product_id=product_id
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"status": "product deactivated"}
