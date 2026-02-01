from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from jose import jwt, JWTError
from uuid import UUID

from starlette.responses import Response

from app.core.config import settings
from app.core.context import(
    current_tenant_id,
    current_user_id,
    current_user_is_admin
)

"""
This middleware is responsible for:
- Extracting JWT from Autherization header
- Verfying token signature and expiration
- Resolving tenant and user context
- Rejecting unauthenticated requests

ALL protected routes depend on this middleware

"""

ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public endpoints (login, docs,health)
        if request.url.path.startswith(("/auth","/docs", "/openapi.json")):
            return await call_next(request)
        
        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid Authorization header"
            )
        
        # Extract tokeen part
        token = auth_header.removeprefix("Bearer ").strip()

        try:
            # Decode and verify JWT
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[ALGORITHM]
            )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        
        # Extract required claims
        tenant_id = payload.get("tenant_id")
        user_id = payload.get("user_id")
        is_admin = payload.get("is_admin", False)

        # Enforce presence of required claims
        if not tenant_id or not user_id:
            raise HTTPException(
                status_code=401,
                detail="Token missing required claims"
            )
        try:
            tenant_uuid = UUID(tenant_id)
            user_uuid = UUID(user_id)

        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token identifiers"
            )
        
        # Store values in request-scoped context
        tenant_token = current_tenant_id.set(tenant_uuid)
        user_token = current_user_id.set(user_uuid)
        admin_token = current_user_is_admin.set(bool(is_admin))

        try:
            # Continue request processing
            response = await call_next(request)
        finally:
            # Cleanup context to prevent leakage
            current_tenant_id.reset(tenant_token)
            current_user_id.reset(user_token)
            current_user_is_admin.reset(admin_token)

        return response
