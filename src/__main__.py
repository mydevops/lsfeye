from src.lib import const
from src.lib.config import settings
from src.lib.gunicorn_runner import GunicornApplication


def main() -> None:
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
