from typing import Any
from typing import Dict

from src.db.bhosts import BhostsModel
from src.lib.plugin.base import PluginBase


class Bhosts(PluginBase):
    def __init__(self) -> None:
        super().__init__(
            cmd="bhosts -o 'host_name status cpuf jl_u max njobs run ssusp "
            "ususp rsv dispatch_window ngpus ngpus_alloc ngpus_excl_alloc "
            "ngpus_shared_alloc ngpus_shared_jexcl_alloc ngpus_excl_avail "
            "ngpus_shared_avail' -json",
            model=BhostsModel,
            unique_key="host_name",
        )

    def prepare_values(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "host_name": record.get("HOST_NAME"),
            "status": record.get("STATUS"),
            "cpuf": record.get("CPUF") or None,
            "jl_u": record.get("JL_U") or None,
            "max": record.get("MAX") or None,
            "njobs": record.get("NJOBS") or None,
            "run": record.get("RUN") or None,
            "ssusp": record.get("SSUSP") or None,
            "ususp": record.get("USUSP") or None,
            "rsv": record.get("RSV") or None,
            "dispatch_window": record.get("DISPATCH_WINDOW") or None,
            "ngpus": record.get("NGPUS") or None,
            "ngpus_alloc": record.get("NGPUS_ALLOC") or None,
            "ngpus_excl_alloc": record.get("NGPUS_EXCL_ALLOC") or None,
            "ngpus_shared_alloc": record.get("NGPUS_SHARED_ALLOC") or None,
            "ngpus_shared_jexcl_alloc": record.get("NGPUS_SHARED_JEXCL_ALLOC")
            or None,
            "ngpus_excl_avail": record.get("NGPUS_EXCL_AVAIL") or None,
            "ngpus_shared_avail": record.get("NGPUS_SHARED_AVAIL") or None,
        }


async def do() -> None:
    await Bhosts().do()
