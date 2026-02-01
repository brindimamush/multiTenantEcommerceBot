from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tenant import Tenant
from app.schemas.branding import BrandingUpdateRequest

"""
Service layer contains business rules.

Endpoints should NOT manipulate models directly

"""

async def get_branding(
        db:AsyncSession,
        tenant_id
):
    """
    Fetch branding configuration for a tenant

    """

    stmt = select(Tenant).where(Tenant.id == tenant_id)
    tenant = (await db.execute(stmt)).scalar_one()

    return tenant

async def update_branding(
        db: AsyncSession,
        tenant_id,
        data: BrandingUpdateRequest,
        logo_url:str | None = None,
):
    """
    Update branding configuration for a tenant.

    Only admins should reach this function

    """

    stmt = select(Tenant).where(Tenant.id == tenant_id)
    tenant = (await db.execute(stmt)).scalar_one()

    # Update theme colors
    tenant.primary_color = data.primary_color
    tenant.secondary_color = data.secondary_color

    # Update logo only if provided
    if logo_url:
        tenant.logo_url = logo_url

    await db.commit()
    await db.refresh(tenant)

    return tenant