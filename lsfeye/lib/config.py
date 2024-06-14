import configparser
from typing import Any

from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from lsfeye.lib import const


class Basic(BaseModel):
    app_name: str
    host: str
    port: int
    workers_count: int
    debug: bool


class Loguru(BaseModel):
    path: str
    filename: str
    level: str
    rotation: str
    format: str


class MySQL(BaseModel):
    dsn: str


class SchedulerLock(BaseModel):
    host: str
    port: int


class IntervalTrigger(BaseModel):
    bqueues: int


class App(BaseModel):
    basic: Basic
    loguru: Loguru
    mysql: MySQL
    scheduler_lock: SchedulerLock
    interval_trigger: IntervalTrigger


def read_config(file_path: str) -> App:
    config = configparser.ConfigParser()
    config.read(file_path)

    mysql_config = config["MYSQL"]

    return App(
        basic=Basic(**config["BASIC"]),
        loguru=Loguru(**config["LOGURU"]),
        mysql=MySQL(
            **{
                "dsn": f"{mysql_config.get('scheme')}"
                "://"
                f"{mysql_config.get('user')}:{mysql_config.get('password')}"
                "@"
                f"{mysql_config.get('host')}:{mysql_config.get('port')}"
                "/"
                f"{mysql_config.get('db')}"
            }
        ),
        scheduler_lock=SchedulerLock(**config["SCHEDULERLOCK"]),
        interval_trigger=IntervalTrigger(**config["INTERVALTRIGGER"]),
    )


settings = read_config(const.CONFIG_PATH)
app: dict[str, Any] = {
    "title": f"{settings.basic.app_name} API",
    "default_response_class": ORJSONResponse,
}
