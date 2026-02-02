# import asyncio
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.session import async_session
# from app.models.tenant import Tenant
# from app.models.user import User

# """
# One-time seed script.
# DO NOT run in production.
# """

# async def seed():
#     async with async_session() as db:  # type: AsyncSession
#         tenant = Tenant(
#             name="Demo Shop",
#             slug="demo-shop",
#             primary_color="#000000",
#             secondary_color="#FFFFFF",
#         )

#         db.add(tenant)
#         await db.flush()  # get tenant.id

#         admin = User(
#             tenant_id=tenant.id,
#             telegram_id="123456789",
#             is_admin=True,
#         )

#         db.add(admin)
#         await db.commit()

# asyncio.run(seed())
