from abc import ABC, abstractmethod
from psutil import cpu_percent
from time import perf_counter, sleep
from threading import Thread
from uuid import uuid4

import numpy as np
from pypapi import papi_low

from settings import settings


class PAPIBase(ABC):
    def __init__(self):
        papi_low.library_init()

    @staticmethod
    def get_component(component_name):
        num = papi_low.num_components()
        for i in range(num):
            cmp = papi_low.get_component_info(i)
            if cmp.name == component_name:
                return i, cmp
        return None, None

    @staticmethod
    def create_eventset(event_names):
        event_set = papi_low.create_eventset()
        event_codes = []
        for name in event_names:
            event_codes.append(papi_low.event_name_to_code(name))

        papi_low.add_events(event_set, event_codes)
        return event_set

    @staticmethod
    def start(eventset):
        papi_low.start(eventset)

    @staticmethod
    def stop(eventset):
        return papi_low.stop(eventset)

    @staticmethod
    def read(eventset):
        return papi_low.read(eventset)

    @abstractmethod
    def start_measurements(self):
        pass

    @abstractmethod
    def stop_measurements(self):
        pass


class LoadBase(ABC):
    def __init__(self):
        self.regions = {}
        with open("regions.csv", "w") as f:
            f.write("name,uuid,start,end,energy(J)\n")

    def start_measurements(self, plot=True):
        if plot:
            with open("power.csv", "w") as f:
                f.write("timestamp,power(W)\n")
            self.run = True
            self.plot_thread = Thread(target=self.plot, daemon=True)
            self.plot_thread.start()

    def stop_measurements(self):
        if self.run:
            self.run = False
            self.plot_thread.join()

    def start_region(self, name):
        region_uuid = uuid4()
        start_t = perf_counter()
        start_m = self.get_power()
        self.regions[region_uuid] = {
            "name": name,
            "power": [start_m],
            "ts": [start_t],
        }
        return region_uuid

    def end_region(self, region_uuid, intermediate=False):
        region = self.regions.pop(region_uuid, None)
        if region is None:
            return None
        end_t = perf_counter()
        end_m = self.get_power()
        region["ts"].append(end_t)
        region["power"].append(end_m)
        n_time = np.array(region["ts"]) - region["ts"][0]
        energy = np.trapz(region["power"], n_time)
        result = {
            "energy": energy,
            "time": end_t - region["ts"][0],
        }
        with open("regions.csv", "a") as f:
            f.write(f"{region['name']},{str(region_uuid)},{region['ts'][0]},{end_t},{energy}\n")

        if intermediate:
            result["power"] = region["power"]
            result["ts"] = list(n_time)
        return result

    def plot(self):
        while self.run:
            f = open("power.csv", "a")
            current = self.get_power()
            current_t = perf_counter()
            for key in self.regions:
                self.regions[key]["power"].append(current)
                self.regions[key]["ts"].append(current_t)
            f.write(f"{current_t},{current}\n")
            previous = current
            previous_t = current_t
            f.close()
            sleep(settings.sampling_rate)
        f.close()

    def get_power(self):
        return self.idle + (cpu_percent() / 100) * (self.stressed - self.idle)
