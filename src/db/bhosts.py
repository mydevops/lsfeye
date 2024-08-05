from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base
from src.db.base import HasCreateTimeMixin
from src.db.base import HasIdMixin
from src.db.base import HasLastUpdateTimeMixin


class BhostsModel(
    HasIdMixin, HasCreateTimeMixin, HasLastUpdateTimeMixin, Base
):
    __tablename__ = "tb_bhosts"

    host_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    cpuf: Mapped[float] = mapped_column(Float, nullable=True)
    jl_u: Mapped[int] = mapped_column(Integer, nullable=True)
    max: Mapped[int] = mapped_column(Integer, nullable=True)
    njobs: Mapped[int] = mapped_column(Integer, nullable=True)
    run: Mapped[int] = mapped_column(Integer, nullable=True)
    ssusp: Mapped[int] = mapped_column(Integer, nullable=True)
    ususp: Mapped[int] = mapped_column(Integer, nullable=True)
    rsv: Mapped[int] = mapped_column(Integer, nullable=True)
    dispatch_window: Mapped[str] = mapped_column(String(1024), nullable=True)
    ngpus: Mapped[int] = mapped_column(Integer, nullable=True)
    ngpus_alloc: Mapped[int] = mapped_column(Integer, nullable=True)
    ngpus_excl_alloc: Mapped[int] = mapped_column(Integer, nullable=True)
    ngpus_shared_alloc: Mapped[int] = mapped_column(Integer, nullable=True)
    ngpus_shared_jexcl_alloc: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    ngpus_excl_avail: Mapped[int] = mapped_column(Integer, nullable=True)
    ngpus_shared_avail: Mapped[int] = mapped_column(Integer, nullable=True)
