from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from schemas import StartBody, StartResponse, EndBody, EndResponse

router = APIRouter()


@router.post("/start", response_model=StartResponse)
async def start_region(request: Request, body: StartBody):
    region_uuid = request.app.state.device.start_region(body.region)
    return {"uuid": region_uuid}


@router.post("/end", response_model=EndResponse)
async def end_region(request: Request, body: EndBody):
    result = request.app.state.device.end_region(
        body.uuid, intermediate=body.intermediate
    )
    if result is None:
        return JSONResponse(
            status_code=404,
            content={"message": "region does not exist"},
        )
    return result
