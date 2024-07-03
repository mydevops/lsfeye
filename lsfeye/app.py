from fastapi import FastAPI

from lsfeye.api.router import api_router
from lsfeye.lib import config
from lsfeye.lib import event
from lsfeye.lib import extension
from lsfeye.lib import middleware


def make_app() -> FastAPI:
    """获取 FastAPI 应用"""

    # 初始化日志等配置
    extension.init()

    app = FastAPI(**config.app)

    # 注册事件
    event.register(app)

    # 注册中间件
    middleware.register(app)

    # 注册路由
    app.include_router(api_router)

    return app
