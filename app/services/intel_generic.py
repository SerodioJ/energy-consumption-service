from time import perf_counter, sleep
from threading import Thread
from uuid import uuid4

import numpy as np

from .base import PAPIBase
from settings import settings


class IntelGeneric(PAPIBase):
    events = [
        "powercap:::ENERGY_UJ:ZONE0",
        "powercap:::MAX_ENERGY_RANGE_UJ:ZONE0",
    ]

    def __init__(self):
        super().__init__()
        self.cmp_id, self.component_info = self.get_component("powercap")
        self.default_eventset = self.create_eventset(self.events)
        self.regions = {}
        with open("regions.csv", "w") as f:
            f.write("name,uuid,start,end,energy(J)\n")

    def plot(self):
        f = open("power.csv", "a")
        previous = self.read(self.default_eventset)[0]
        previous_t = perf_counter()
        f.write(f"{previous_t},{previous},\n")
        f.close()
        sleep(settings.sampling_rate)
        while self.run:
            f = open("power.csv", "a")
            current = self.read(self.default_eventset)[0]
            current_t = perf_counter()
            power = (current - previous) / ((current_t - previous_t) * 1e6)
            for key in self.regions:
                self.regions[key]["power"].append(power)
                self.regions[key]["ts"].append(current_t)
            f.write(f"{current_t},{current},{power}\n")
            previous = current
            previous_t = current_t
            f.close()
            sleep(settings.sampling_rate)
        f.close()

    def start_measurements(self, plot=False):
        self.start(self.default_eventset)
        if plot:
            with open("power.csv", "w") as f:
                f.write("timestamp,energy(uJ),power(W)\n")
            self.run = True
            self.plot_thread = Thread(target=self.plot, daemon=True)
            self.plot_thread.start()

    def stop_measurements(self):
        if self.run:
            self.run = False
            self.plot_thread.join()
        self.stop(self.default_eventset)

    def start_region(self, name):
        region_uuid = uuid4()
        start_t = perf_counter()
        start_m = self.read(self.default_eventset)[0]
        self.regions[region_uuid] = {
            "name": name,
            "start": (start_t, start_m),
            "power": [],
            "ts": [],
        }
        return region_uuid

    def end_region(self, region_uuid, intermediate=False):
        end_t = perf_counter()
        end_m = self.read(self.default_eventset)[0]
        region = self.regions.pop(region_uuid, None)
        if region is None:
            return None
        energy =  (end_m - region["start"][1]) / 1e6
        result = {
            "energy": energy,
            "time": end_t - region["start"][0],
        }
        with open("regions.csv", "a") as f:
            f.write(
                f"{region['name']},{str(region_uuid)},{region['start'][0]},{end_t},{energy}\n"
            )

        if intermediate:
            result["power"] = region["power"]
            result["ts"] = list(np.array(region["ts"]) - region["start"][0])
        return result
