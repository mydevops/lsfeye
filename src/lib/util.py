from __future__ import annotations

import socket
import subprocess
import time
from typing import Any

from src.lib import const
from src.lib import enum
from src.lib.config import settings


def make_response_ok(resp: dict[str, Any] | None = None) -> dict[str, Any]:
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


def execute_shell_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Error: {result.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing command: {e.stderr.strip()}")
