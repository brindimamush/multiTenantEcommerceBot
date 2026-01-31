import hmac
import hashlib
from urllib.parse import parse_qsl
from typing import Dict

"""
Telegram signs initData using bot token.

If verification fails:
- The request is forged
- Must be rejected
"""

def verify_telegram_init_data(
        init_data:str,
        bot_token:str
) -> Dict[str, str]:
    """
    Docstring for verify_telegram_init_data
    
    Verifies Telegram WebApp initData.

    Steps (Telegram spec):
    1. Parse key-value pairs
    2. Extract hash
    3. Create data_check_string
    4. Generate secret key from bot token
    5. Compare HMAC-SHA256 signatures

    :param init_data: Description
    :type init_data: str
    :param bot_token: Description
    :type bot_token: str
    :return: Description
    :rtype: Dict[str, str]
    """

    # parse query string into list of tuples
    parsed_data = dict(parse_qsl(init_data))

    # Extract hash sent by Telegram
    received_hash = parsed_data.pop("hash", None)

    if not received_hash:
        raise ValueError("Missing Telegram hash")
    
    # Sort parameters alphabetically
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items())
    )

    # Telegram requires SHA256(bot_token) as secret key
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    # Compute HMAC-SHA256
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid Telegram signature")
    
    return parsed_data