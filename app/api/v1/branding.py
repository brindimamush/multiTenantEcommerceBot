from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_tenant_db
from app.core.context import current_tenant_id, current_user_is_admin
from app.schemas.branding import BrandingResponse, BrandingUpdateRequest
from app.services.branding import get_branding, update_branding
from app.utils.file_upload import save_logo

router = APIRouter(prefix="/branding", tags=["branding"])

@router.get("/", response_model=BrandingResponse)
async def get_branding_config(
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Public endpoint.

    Used by frontend on app load to apply theme.
    
    """
    tenant_id = current_tenant_id.get()
    tenant = await get_branding(db, tenant_id)

    return BrandingResponse(
        primary_color=tenant.primary_color,
        secondary_color=tenant.secondary_color,
        logo_url=tenant.logo_url,
    )

@router.put("/")
async def update_branding_config(
    data: BrandingUpdateRequest = Depends(),
    logo: UploadFile | None = File(default=None),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Admin-only endpoint.

    Allows tenant owner to rebrand instantly.
    """
    # Enforce admin access
    if not current_user_is_admin.get():
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    logo_url = None

    # Save logo if provided
    if logo:
        logo_url = await save_logo(logo)

    tenant_id = current_tenant_id.get()

    await update_branding(
        db=db,
        tenant_id=tenant_id,
        data=data,
        logo_url=logo_url
    )

    return {"status": "branding updated"}