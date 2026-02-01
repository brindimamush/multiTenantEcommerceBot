from contextvars import ContextVar
from uuid import UUID

"""
ContextVar allows to store data that is:
- Scoped to the current request
- Safe in async environments
- Accessible anywhere in the codebase

This is how we avoid passing tenant_id manually everywhere.

Request-scoped contaxt variables.

These values exist ONLY during the lifetime of a request.
They are safe for async code and cannot leak between users.
"""

current_tenant_id: ContextVar[UUID | None] = ContextVar(
    "current_tenant_id",
    default=None
)

# Current authenticated user identifier
current_user_id: ContextVar[UUID | None] = ContextVar(
    "current_user_id",
    default=None
)

# Role flag for authorization checks
current_user_is_admin: ContextVar[bool] = ContextVar(
    "current_user_is_admin",
    default=False
)