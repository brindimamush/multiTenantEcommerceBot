from fastapi import FastAPI
from app.middlewares.auth import AuthMiddleware
from app.middlewares.tenant import TenantMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.branding import router as branding_router
from app.api.v1.products import router as products_router
def create_app() -> FastAPI:
    """
    Docstring for create_app
    Application factory.

    Middleware order is CRITICAL:
    1. AuthMiddleware -> resolves JWT
    2. TenantMiddleware -> enforces tenant presence

    Middleware is registered here so:
    - It applies globally
    - Order is controlled
    :return: Description
    :rtype: FastAPI
    """
    app = FastAPI(
        title="Telegram Multitenant Commerce",
        version="0.1.0"
    )
    # Authentication MUST come first
    app.add_middleware(AuthMiddleware)

    # Tenant enforcement comes after auth
    app.add_middleware(TenantMiddleware)

    # Authentication routes
    app.include_router(auth_router)

    #Branding routes
    app.include_router(branding_router)

    # Products router
    app.include_router(products_router)

    return app

app = create_app()