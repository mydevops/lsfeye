from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class HTTPResponse(BaseModel):
    """HTTP 通用返回格式"""

    retcode: int = Field(description="返回状态码，0 成功，其他均为失败")
    msg: Optional[str] = Field(None, description="成功文本")
    error: Optional[str] = Field(None, description="错误描述")
    resp: Optional[Dict[Any, Any]] = Field({}, description="数据")
