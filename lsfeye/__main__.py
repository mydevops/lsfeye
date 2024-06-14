from lsfeye.lib import const
from lsfeye.lib.config import settings
from lsfeye.lib.gunicorn_runner import GunicornApplication


def main() -> None:
    """主程序入口"""
    GunicornApplication(
        app=const.MAIN_APP_PATH,
        host=settings.basic.host,
        port=settings.basic.port,
        workers=settings.basic.workers_count,
        loglevel=settings.loguru.level.lower(),
        factory=True,
    ).run()


if __name__ == "__main__":
    main()
