import socket
import time
from typing import Any
from typing import Dict

from lsfeye.lib import const
from lsfeye.lib import enum
from lsfeye.lib.config import settings


def make_response_ok(resp: Dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "retcode": enum.HTTPStatusCode.SUCCESS.value,
        "msg": const.MAKE_RESPONSE_OK_MSG,
        "resp": resp if resp else {},
        "error": "",
    }


def make_response_not_ok(error: str) -> dict[str, Any]:
    return {
        "retcode": enum.HTTPStatusCode.FAILURE.value,
        "error": error,
        "resp": {},
    }


def scheduler_lock() -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((settings.scheduler_lock.host, settings.scheduler_lock.port))
    except socket.error:
        return True
    else:
        time.sleep(1)
        return False
