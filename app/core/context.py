from contextvars import ContextVar
from uuid import UUID

"""
ContextVar allows to store data that is:
- Scoped to the current request
- Safe in async environments
- Accessible anywhere in the codebase

This is how we avoid passing tenant_id manually everywhere.
"""

current_tenant_id: ContextVar[UUID | None] = ContextVar(
    "current_tenant_id",
    default=None
)