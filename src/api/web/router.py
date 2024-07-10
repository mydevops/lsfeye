from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.web import schema
from src.api.web import service
from src.db.base import get_db_session
from src.lib import schema as common_schema
from src.lib import util as common_util


router = APIRouter()


@router.post("/query", response_model=common_schema.HTTPResponse)
async def test(
    request: Request,
    body: schema.Query,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    logger.info(f"收到 SQL 查询任务: {body} {request.headers}")
    return common_util.make_response_ok(
        resp=await service.query(session, body)
    )
