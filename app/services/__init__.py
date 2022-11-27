from .rasp import RaspPI3Bplus, RaspPI4B
from .intel_generic import IntelGeneric

service_dict = {
    1: {"default": IntelGeneric},
    7: {
        "default": RaspPI4B,
        "rasp4": RaspPI4B,
        "rasp3": RaspPI3Bplus,
    },
}
