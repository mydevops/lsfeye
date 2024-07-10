from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base
from src.db.base import HasCreateTimeMixin
from src.db.base import HasIdMixin
from src.db.base import HasLastUpdateTimeMixin


class BQueuesModel(
    HasIdMixin, HasCreateTimeMixin, HasLastUpdateTimeMixin, Base
):
    __tablename__ = "tb_bqueues"

    queue_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    max: Mapped[int] = mapped_column(Integer, nullable=True)
    jl_u: Mapped[int] = mapped_column(Integer, nullable=True)
    jl_p: Mapped[int] = mapped_column(Integer, nullable=True)
    jl_h: Mapped[int] = mapped_column(Integer, nullable=True)
    njobs: Mapped[int] = mapped_column(Integer, nullable=True)
    pend: Mapped[int] = mapped_column(Integer, nullable=True)
    run: Mapped[int] = mapped_column(Integer, nullable=True)
    susp: Mapped[int] = mapped_column(Integer, nullable=True)
    rsv: Mapped[int] = mapped_column(Integer, nullable=True)
    ususp: Mapped[int] = mapped_column(Integer, nullable=True)
    ssusp: Mapped[int] = mapped_column(Integer, nullable=True)
    nice: Mapped[int] = mapped_column(Integer, nullable=True)
