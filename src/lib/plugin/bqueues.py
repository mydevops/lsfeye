from typing import Any
from typing import Dict

from src.db.bqueues import BQueuesModel
from src.lib.plugin.base import PluginBase


class Bqueues(PluginBase):
    def __init__(self) -> None:
        super().__init__(
            cmd="bqueues -o 'queue_name description priority status max jl_u "
            "jl_p jl_h njobs pend run susp rsv ususp ssusp nice' -json",
            model=BQueuesModel,
            unique_key="queue_name",
        )

    def prepare_values(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "queue_name": record.get("QUEUE_NAME"),
            "description": record.get("DESCRIPTION"),
            "priority": record.get("PRIORITY") or None,
            "status": record.get("STATUS"),
            "max": record.get("MAX") or None,
            "jl_u": record.get("JL_U") or None,
            "jl_p": record.get("JL_P") or None,
            "jl_h": record.get("JL_H") or None,
            "njobs": record.get("NJOBS") or None,
            "pend": record.get("PEND") or None,
            "run": record.get("RUN") or None,
            "susp": record.get("SUSP") or None,
            "rsv": record.get("RSV") or None,
            "ususp": record.get("USUSP") or None,
            "ssusp": record.get("SSUSP") or None,
            "nice": record.get("NICE") or None,
        }


async def do() -> None:
    await Bqueues().do()
