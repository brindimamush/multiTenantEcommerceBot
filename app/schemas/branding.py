from pydantic import BaseModel, Field

"""
Schemas define what the frontend is allowed to see or send

They protect your database models from leaking directly.
"""

class BrandingResponse(BaseModel):
    """
    Public branding configuration sent to frontend.
    """

    primary_color: str = Field(..., examples=["#0A84FF"])
    secondary_color: str = Field(..., examples=["#FFFFFF"])
    logo_url: str | None

class BrandingUpdateRequest(BaseModel):
    """
    Branding update payload (admin only).

    """

    primary_color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: str = Field(..., pattern= r"^#[0-9A-Fa-f]{6}$")