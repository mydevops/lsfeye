import contextlib
import importlib
import os
from datetime import datetime
from typing import Any
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.schema import CreateTable

from lsfeye.lib.config import settings


def init() -> None:
    for table in os.listdir(os.path.dirname(__file__)):
        if table.endswith(".py") and table not in ["__init__.py", "base.py"]:
            table_name = table.split(".py")[0]
            print("table_name", table_name, f"lsfeye.db.{table_name}")
            importlib.import_module(f"lsfeye.db.{table_name}")


class Base(DeclarativeBase):
    @classmethod
    def show_create_table_sql(cls) -> CreateTable:
        return CreateTable(cls.__table__)


class HasIdMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        sort_order=-1,
        comment="数据库主键",
    )


class HasCreateTimeMixin:
    create_time: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        sort_order=99,
        comment="创建时间",
    )


class HasLastUpdateTimeMixin:
    last_update_time: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        sort_order=100,
        comment="最后一次更新时间",
    )


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self.engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self) -> Any:
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()

        self.engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    settings.mysql.dsn,
    {
        "echo": settings.basic.debug,
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,
    },
)


async def get_db_session() -> Any:
    async with sessionmanager.session() as session:
        yield session
