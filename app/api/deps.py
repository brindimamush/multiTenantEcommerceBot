from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.core.database import get_db
from app.core.context import current_tenant_id

async def get_tenant_id(
        db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    """
    Docstring for get_tenant_id
    
    Dependency that guarantees:

    - Tenant is resolved
    - Database access is tenant-aware

    All business endpoints should use THIS instead of get_db.
    :param db: Description
    :type db: AsyncSession
    :return: Description
    :rtype: AsyncSession
    """

    tenant_id = current_tenant_id.get()

    if tenant_id is None:
        raise HTTPException(
            status_code=400,
            detail="Tenant not resolved"
        )
    
    # Attach tenant_id to session info for repositories
    db.info["tenant_id"] = tenant_id

    return db

async def get_tenant_db(
        db:AsyncSession = Depends(get_db),
) -> AsyncSession:
    """
    Returns a database session with tenant context attached.

    Guarantees:
    - Tenan is resolved by middleware
    - Queries can safely enforce tenant isolation
    """
    tenant_id = current_tenant_id.get()

    if tenant_id is None:
        raise HTTPException(
            status_code=400,
            detail="Tenant context not available"
            )
    # Attach tenant_id to session info
    db.info["tenant_id"] = tenant_id

    return db