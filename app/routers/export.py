from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/power", response_class=FileResponse)
async def export_power():
    return "power.csv"


@router.get("/regions", response_class=FileResponse)
async def export_regions():
    return "regions.csv"
