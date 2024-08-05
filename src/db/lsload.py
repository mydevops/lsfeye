from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base
from src.db.base import HasCreateTimeMixin
from src.db.base import HasIdMixin
from src.db.base import HasLastUpdateTimeMixin


class LsloadModel(
    HasIdMixin, HasCreateTimeMixin, HasLastUpdateTimeMixin, Base
):
    __tablename__ = "tb_lsload"

    host_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    r15s: Mapped[float] = mapped_column(Float, nullable=True)
    r1m: Mapped[float] = mapped_column(Float, nullable=True)
    r15m: Mapped[float] = mapped_column(Float, nullable=True)
    ut: Mapped[float] = mapped_column(Float, nullable=True)
    pg: Mapped[float] = mapped_column(Float, nullable=True)
    ls: Mapped[float] = mapped_column(Integer, nullable=True)
    it: Mapped[float] = mapped_column(Integer, nullable=True)
    io: Mapped[float] = mapped_column(Integer, nullable=True)
    tmp: Mapped[float] = mapped_column(Float, nullable=True)
    swp: Mapped[float] = mapped_column(Float, nullable=True)
    mem: Mapped[float] = mapped_column(Float, nullable=True)
