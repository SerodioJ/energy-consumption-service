# Idle and Stressed values from http://www.pidramble.com/wiki/benchmarks/power-consumption

from .base import LoadBase


class RaspPI4B(LoadBase):
    n_cpu = 4
    idle = 2.7
    stressed = 6.4


class RaspPI3Bplus(LoadBase):
    num_cores = 4
    idle = 1.9
    stressed = 5.1


class RaspPI3B(LoadBase):
    num_cores = 4
    idle = 1.4
    stressed = 3.7


class RaspPI2B(LoadBase):
    num_cores = 4
    idle = 1.1
    stressed = 2.1
