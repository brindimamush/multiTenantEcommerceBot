from fastapi import FastAPI
from app.middlewares.tenant import TenantMiddleware

def create_app() -> FastAPI:
    """
    Docstring for create_app
    Application factory.

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

    # Tenant middleware MUST rub before routers
    app.add_middleware(TenantMiddleware)

    return app

app = create_app()