from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.services.telegram_auth import verify_telegram_init_data
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/telegram-login")
async def telegram_login(
    init_data:str,
    tenant_slug:str,
    db: AsyncSession = Depends(get_db),
):
    """
    Docstring for telegram_login
    Authenticates a user using Telegram Webapp initData.

    Responsibilities:
    - Resolve tenant
    - Verify Telegram signature
    - Create or fetch user
    - Issue JWT

    :param init_data: Description
    :type init_data: str
    :param tenant_slug: Description
    :type tenant_slug: str
    :param db: Description
    :type db: AsyncSession
    """

    # Resolve tenant using slug (safe public identifier)
    tenant_stmt = select(Tenant).where(
        Tenant.slug == tenant_slug,
        Tenant.is_active == True
    )
    tenant = (await db.execute(tenant_stmt)).scalar_one_or_none()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Verify Telegram signature using tenant's bot token
    try:
        telegram_data = verify_telegram_init_data(
            init_data=init_data,
            bot_token=str(tenant.telegram_bot_token),
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    # Extract Telegram user info
    telegram_user_id = telegram_data.get("user[id]")
    full_name = telegram_data.get("user[first_name]")

    if not telegram_user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid Telegram user data"
        )
    
    # Feth or create user within this tenant
    user_stmt = select(User).where(
        User.tenant_id == tenant.id,
        User.telegram_user_id == telegram_user_id
    )
    user = (await db.execute(user_stmt)).scalar_one_or_none()

    if not user:
        user = User(
            tenant_id=tenant.id,
            telegram_user_id=telegram_user_id,
            full_name=full_name,
            is_admin=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Issue JWT containing tenant + user context
    access_token = create_access_token(
        data={
            "tenant_id": str(tenant.id),
            "user_id": str(user.id),
            "is_admin": user.is_admin,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }