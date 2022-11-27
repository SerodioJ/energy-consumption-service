from fastapi import FastAPI
from pypapi import papi_low

from routers import region, export
from services import service_dict
from settings import settings

app = FastAPI()

papi_low.library_init()

hardware = papi_low.get_hardware_info()

app.state.device = service_dict[hardware.vendor][settings.hardware_config]()

app.state.device.start_measurements(plot=True)

app.include_router(region.router, prefix="/region")
app.include_router(export.router, prefix="/export")
