import importlib
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from lsfeye.lib.config import settings


def do() -> None:
    scheduler = AsyncIOScheduler()
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            plugin_name = filename[:-3]
            module = importlib.import_module(
                f"lsfeye.lib.plugin.{plugin_name}"
            )

            scheduler.add_job(
                getattr(module, "do"),
                IntervalTrigger(
                    seconds=getattr(settings.interval_trigger, plugin_name)
                ),
            )
    scheduler.start()
