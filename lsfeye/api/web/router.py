from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from lsfeye.api.web import service
from lsfeye.db.base import get_db_session
from lsfeye.lib import schema as common_schema
from lsfeye.lib import util as common_util


router = APIRouter()


@router.post("", response_model=common_schema.HTTPResponse)
async def test(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    logger.info("log")
    return common_util.make_response_ok(resp=await service.test())
