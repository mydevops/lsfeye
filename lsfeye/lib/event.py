from typing import Awaitable
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from lsfeye.db import base as db
from lsfeye.db.base import Base
from lsfeye.db.base import sessionmanager
from lsfeye.lib import plugin
from lsfeye.lib import util


def _register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    """
    程序启动时操作。

    Args:
        app: FastAPI 实例

    Returns:
        执行的函数。
    """

    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        if util.scheduler_lock() is False:
            db.init()
            async with sessionmanager.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            await plugin.do()

        app.middleware_stack = app.build_middleware_stack()

    return _startup


def _register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    """
    程序关闭时操作。

    Args:
        app: FastAPI 实例

    Returns:
        执行的函数。
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        if sessionmanager.engine is not None:
            await sessionmanager.close()
        logger.remove()

    return _shutdown


def register(app: FastAPI) -> None:
    """
    事件的统一注册函数。

    Args:
        app: FastAPI 实例
    """
    _register_startup_event(app)
    _register_shutdown_event(app)
