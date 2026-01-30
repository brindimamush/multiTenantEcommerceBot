from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import current_tenant_id
from uuid import UUID

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Docstring for TenantMiddleware

    Middleware responsible for:

    - Resolving tenant from request
    - Enforcing tenant presence
    - Attaching tenant_id to request context

    This will run BEFORE any endpoint logic.
    """

    async def dispatch(self, request: Request, call_next):
        # Try to extract tenant_id from request state
        #(will be set by auth layer later)
        tenant_id = request.headers.get("X-Tenant-ID")

        # In production, tenant_id should NEVER come directly from client
        # This is temporary and will be replaced by JWT resolution
        if not tenant_id:
            raise HTTPException(
                status_code=400,
                detail="Tenant context missing"
            )
        try:
            #validate UUID format early
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid tenant Identifier"
            )
        
        #store tenant in request-scoped context
        token = current_tenant_id.set(tenant_uuid)

        try:
            # continue processing request
            response = await call_next(request)
        finally:
            # Clean up context after request completes
            current_tenant_id.reset(token)
        return response