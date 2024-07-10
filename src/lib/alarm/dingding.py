import base64
import hashlib
import hmac
import time
import urllib.parse

import httpx
from loguru import logger

from src.lib import config
from src.lib import const


async def send(settings: config.App, content: str) -> None:
    timestamp = str(round(time.time() * 1000))
    hmac_code = hmac.new(
        settings.alarm.secret.encode("utf-8"),
        f"{timestamp}\n{settings.alarm.secret}".encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    async with httpx.AsyncClient(
        headers=const.HTTP_JSON_HEADER, timeout=const.HTTP_TIMEOUT
    ) as client:
        try:
            await client.post(
                url=settings.alarm.webhook,
                params={
                    "timestamp": timestamp,
                    "sign": urllib.parse.quote_plus(
                        base64.b64encode(hmac_code).decode("utf-8")
                    ),
                },
                json={
                    "msgtype": "text",
                    "text": {"content": content},
                },
            )
        except Exception as e:
            logger.exception(e)
