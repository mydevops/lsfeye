from typing import Any
from typing import Dict

from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.api.web import schema


async def query(session: AsyncSession, body: schema.Query) -> Dict[str, Any]:
    result = await session.execute(text(body.sql))

    rows = result.fetchall()

    columns = result.keys()

    rows_as_dicts = [
        {column: getattr(row, column) for column in columns} for row in rows
    ]
    return {"data": rows_as_dicts}
