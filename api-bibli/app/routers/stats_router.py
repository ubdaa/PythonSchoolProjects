from fastapi import APIRouter

from schemas.common import StatsResponse

router = APIRouter(prefix="/stats", tags=["Statsistics"])

@router.get("/", response_model=StatsResponse)
async def get_statistics():
    