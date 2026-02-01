from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import current_tenant_id
from uuid import UUID

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Docstring for TenantMiddleware

    Tenant middleware now ENFORCES that:
    - Auth middleware already resolved tenant_id
    - No request proceeds without tenant context

    Middleware responsible for:

    - Resolving tenant from request
    - Enforcing tenant presence
    - Attaching tenant_id to request context

    This will run BEFORE any endpoint logic.
    """

    async def dispatch(self, request: Request, call_next):
        # Try to extract tenant_id from request state
        #(will be set by auth layer later)
        #tenant_id = request.headers.get("X-Tenant-ID")
        # Public routes do not require tenant context
        if request.url.path.startswith(("/auth", "/docs","/openapi")):
            return await call_next(request)
        
        tenant_id = current_tenant_id.get()
        # In production, tenant_id should NEVER come directly from client
        # This is temporary and will be replaced by JWT resolution
        if tenant_id is None:
            raise HTTPException(
                status_code=400,
                detail="Tenant context not resolved"
            )
        #try:
            #validate UUID format early
            #tenant_uuid = UUID(tenant_id)
        #except ValueError:
          #  raise HTTPException(
          #      status_code=400,
           #     detail="Invalid tenant Identifier"
           # )
        
        #store tenant in request-scoped context
        #token = current_tenant_id.set(tenant_uuid)

        #try:
            # continue processing request
            #response = await call_next(request)
        #finally:
            # Clean up context after request completes
            #current_tenant_id.reset(token)

        # Tenant is already validated by JWT middleware
        return await call_next(request)