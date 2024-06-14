from typing import Any

from pydantic import BaseModel
from pydantic import Field


class HTTPResponse(BaseModel):
    """HTTP 通用返回格式"""

    retcode: int = Field(description="返回状态码，0 成功，其他均为失败")
    msg: str | None = Field(None, description="成功文本")
    error: str | None = Field(None, description="错误描述")
    resp: dict[Any, Any] | None = Field({}, description="数据")
