
from functools import wraps

import numpy as np

# pythran export __method__Transmitter____call__(float, float[])


def __for_method__Transmitter____call__(self_freq, inp):
    return inp * np.exp(np.arange(len(inp))*self_freq*1j)


def __method__Transmitter____call__(self, inp):
    self_freq = self.freq
    return __for_method__Transmitter____call__(self_freq, inp)


def __call__(self, inp: "float[]"):
    """My docstring"""
    return inp * np.exp(np.arange(len(inp))*self.freq*1j)


class Transmitter():

    freq: float

    def __init__(self, freq):
        self.freq = float(freq)

    __call__ = wraps(__call__)(__method__Transmitter____call__)