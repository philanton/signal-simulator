from math import sin, pi

import matplotlib.pyplot as plt
import numpy as np


def data_source_function(**params):
    """"""
    router = {
        0: lambda params=params: garmonic_signal(
            bytes=params["bytes"],
            amp=params["amplitude"],
            freq=params["frequency"],
            phase=params["phase"],
            periods=params["periods_per_symbol"],
            steps=params["counts_per_period"]
        ),
        1: lambda params=params: manchester_code(
            bytes=params["bytes"],
            amp=params["amplitude"],
            steps=params["counts_per_symbol"]
        )
    }

    values = list(router.get(params["type"], lambda: [])())
    t, y = np.transpose(values)

    return t, y


def interference_function(**params):
    """"""
    router = {
        0: lambda params=params: white_noise(
            amp=params["amplitude"],
            steps=params["steps"]
        )
    }

    y = router.get(params["type"], lambda: [])()

    return y


def connection_line_function(**params):
    """"""
    y = params["signal_values"] * params["signal_coef"]
    y += params["infr_values"] * params["infr_coef"]

    return y


def reference_ds_function(**params):
    """"""
    y = find_ds(params["rds"], None)

    return y if isinstance(y, list) else []


def clock_gen_function(**params):
    y = np.ones(params["total_counts"])

    for i in range(params["total_counts"] // params["counts_per_symbol"]):
        y[i * params["counts_per_symbol"]] = 0

    return y


def correlator_function(**params):
    """"""
    y = np.array(list(accumulative_sum(
        params["cl_values"],
        params["rds_values"],
        params["cg_values"],
        params["delta_t"]
    )))

    return y


def decision_device_function(**params):
    """"""
    correlated = params["corr_values"]
    symbol_count = params["symbol_count"]
    
    symbols_encoded = np.split(correlated, symbol_count)
    y = [np.sum(enc > 0) - np.sum(enc <= 0) for enc in symbols_encoded]

    return y


def get_default_values(abbr, **params):
    """"""
    router = {
        "Infr": default_infr_with_time,
        "RDS": default_rds_with_time,
    }

    t, y = list(router.get(abbr, lambda **params: ([], []))(**params))

    return t, y


def default_infr_with_time(**params):
    """"""
    steps = params["counts_per_symbol"]
    t = np.arange(steps)

    params.update({"steps": steps})
    y = interference_function(**params)

    return t, y


def default_rds_with_time(**params):
    """"""
    steps = params["counts_per_symbol"]
    t = np.arange(steps)
    y = np.zeros(steps)

    return t, y


def garmonic_signal(bytes, amp, freq, phase, periods, steps):
    """"""
    count = 0
    total_counts = counts = periods * steps

    for bit in bytes:
        bit = int(bit)
        while count < total_counts:
            t = count / freq / steps
            y = amp * sin(2 * pi * freq * t + phase * pi) if bit else 0
            yield t, y
            count += 1
        total_counts += counts


def manchester_code(bytes, amp, steps, sample_time=0.001):
    """"""
    count = 0
    total_steps = steps

    for bit in bytes:
        bit = int(bit)
        while count < total_steps:
            t = count * sample_time
            y = -amp if bit else amp
            if count > total_steps - steps / 2:
                y *= -1
            yield t, y
            count += 1
        total_steps += steps


def white_noise(amp, steps):
    """"""
    return np.random.normal(0, amp / 2.355, size=steps)


def find_ds(this_block, source):
    """"""
    for block in this_block.neighbors:
        if block.config["abbr"] == "DS":
            return block.store.values[:]
        elif block != source:
            values = find_ds(block, this_block)
            print(values)
            if isinstance(values, list):
                return values
    return None


def accumulative_sum(list_a, list_b, list_c, delta_t):
    """"""
    s = 0
    for a, b, c in zip(list_a, list_b, list_c):
        s += a * b * delta_t
        s *= c
        yield s


# samples = white_noise(5, 3000)
# plt.plot(samples)
# plt.show()
