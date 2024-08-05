from typing import Any
from typing import Dict

from src.db.lsload import LsloadModel
from src.lib.plugin.base import PluginBase


class Lsload(PluginBase):
    def __init__(self) -> None:
        super().__init__(
            cmd="lsload -o 'HOST_NAME status r15s r1m r15m ut pg ls it io tmp "
            "swp mem' -json",
            model=LsloadModel,
            unique_key="host_name",
        )

    def prepare_values(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "host_name": record.get("HOST_NAME"),
            "status": record.get("status"),
            "r15s": record.get("r15s") or None,
            "r1m": record.get("r1m") or None,
            "r15m": record.get("r15m") or None,
            "ut": record.get("ut", "").strip("%") or None,
            "pg": record.get("pg") or None,
            "ls": record.get("ls") or None,
            "it": record.get("it") or None,
            "io": record.get("io") or None,
            "tmp": record.get("tmp", "").strip("M") or None,
            "swp": record.get("swp", "").strip("M") or None,
            "mem": record.get("mem", "").strip("M") or None,
        }


async def do() -> None:
    await Lsload().do()
