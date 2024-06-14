from typing import Any

from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from uvicorn_worker import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "lifespan": "on",
        "factory": True,
    }


class GunicornApplication(BaseApplication):
    def __init__(
        self,
        app: str,
        host: str,
        port: int,
        workers: int,
        **kwargs: Any,
    ) -> None:
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "lsfeye.lib.gunicorn_runner.UvicornWorker",
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self) -> str:
        return import_app(self.app)

    def on_starting(self) -> None:
        print("gunicorn starting...")
