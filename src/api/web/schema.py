from pydantic import BaseModel
from pydantic import Field


class Query(BaseModel):
    """SQL 查询结果"""

    sql: str = Field(description="SQL 语句")
