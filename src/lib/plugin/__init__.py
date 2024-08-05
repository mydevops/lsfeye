import importlib
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.lib.config import settings


async def do() -> None:
    scheduler = AsyncIOScheduler()
    for filename in os.scandir(os.path.dirname(__file__)):
        if (
            filename.name.endswith(".py")
            and filename.name != "__init__.py"
            and filename.name != "base.py"
        ):
            plugin_name = filename.name[:-3]
            module = importlib.import_module(f"src.lib.plugin.{plugin_name}")

            scheduler.add_job(
                getattr(module, "do"),
                IntervalTrigger(
                    seconds=getattr(settings.interval_trigger, plugin_name)
                ),
            )
    scheduler.start()
