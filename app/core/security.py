from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

"""
This file centralizes all security-related logic.

why:

- Avoid duplicated crypto logic
- Easier audits
- Easier rotation of secrets
"""

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(data: dict) -> str:
    """
    Docstring for create_access_token
    
    Creates a signed JWT containing user and tenant context.

    The token is:
    - Stateless
    - Self-contained
    - Verifiable without DB hit

    :param data: Description
    :type data: dict
    :return: Description
    :rtype: str
    """
    to_encode = data.copy()

    # Add expiration to token
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})

    #Sign token using server secret
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )

    return encoded_jwt