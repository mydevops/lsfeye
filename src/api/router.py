from fastapi import APIRouter

from src.api.web.router import router as web_router_api_v1
from src.lib.enum import ApiVersion


api_router = APIRouter()

api_router.include_router(
    web_router_api_v1,
    prefix=f"/api/v{ApiVersion.VERSION_1.value}",
)


@api_router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
