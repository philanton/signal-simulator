from math import sin, pi

import matplotlib.pyplot as plt
import numpy as np


def data_source_function(**params):
    """"""
    router = {
        0: lambda params=params: garmonic_signal(
            bit=params["bit"],
            amp=params["amplitude"],
            freq=params["frequency"],
            phase=params["phase"],
            periods=params["periods_per_symbol"],
            steps=params["counts_per_period"]
        ),
        1: lambda params=params: manchester_code(
            bit=params["bit"],
            amp=params["amplitude"],
            steps=params["counts_per_symbol"]
        )
    }

    values = list(router[params["type"]]())
    plt.plot(*np.transpose(values))
    plt.show()

    return values


def interference_function(**params):
    """"""


def connection_line_function(**params):
    """"""


def reference_ds_function(**params):
    """"""


def correlator_function(**params):
    """"""


def garmonic_signal(bit, amp, freq, phase, periods, steps):
    """"""
    count = 0
    counts = periods * steps

    while count < counts:
        t = count / freq / steps
        y = amp * sin(2 * pi * freq * t + phase * pi) if bit else 0
        yield t, y
        count += 1


def manchester_code(bit, amp, steps, sample_time=0.05):
    """"""
    count = 0

    while count < steps:
        t = count * sample_time
        y = -amp if bit else amp
        if count > steps / 2:
            y *= -1
        yield t, y
        count += 1
