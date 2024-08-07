from fastapi import FastAPI

from src.api.router import api_router
from src.lib import config
from src.lib import event
from src.lib import extension
from src.lib import middleware


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
