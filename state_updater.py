import numpy as np

import functions as fn

class StateUpdater():
    """"""
    def __init__(self, block):
        """"""
        self.store = {}
        self.stages = [
            self.creating,
            self.addition,
            self.correlating,
            self.decisioning
        ]
        self.init_system(block)

    def init_system(self, block):
        """"""
        find_all_blocks_in_system(self.store, block)

        for block in self.store.values():
            block.store.done = False

        for stage in self.stages:
            try:
                stage()
            except KeyError:
                break

        for abbr, block in self.store.items():
            if not block.store.done:
                args = block.config["values"].copy()
                t, y = fn.get_default_values(abbr, **args)
                block.store.times = t[:]
                block.store.values = y[:]
                block.store.done = True

    def creating(self):
        """"""
        ds = self.store["DS"]

        args = ds.config["values"].copy()
        t, y = fn.data_source_function(**args)
        ds.store.values = y[:]

        for block in self.store.values():
            block.store.times = t[:]

        ds.store.done = True

    def addition(self):
        """"""
        ds = self.store["DS"]
        infr = self.store["Infr"]
        cl = self.store["CL"]

        args = infr.config["values"].copy()
        args.update({"steps": len(infr.store.times)})
        y = fn.interference_function(**args)
        infr.store.values = y[:]
        infr.store.done = True

        args = cl.config["values"].copy()
        args.update({
            "signal_values": ds.store.values[:],
            "infr_values": infr.store.values[:]
        })
        y = fn.connection_line_function(**args)
        cl.store.values = y[:]
        cl.store.done = True

    def correlating(self):
        """"""
        ds = self.store["DS"]
        rds = self.store["RDS"]
        cl = self.store["CL"]
        cg = self.store["CG"]
        corr = self.store["Corr"]

        args = ds.config["values"].copy()
        args.update({"bytes": len(args["bytes"]) * "1"})
        _, y = fn.data_source_function(**args)
        rds.store.values = y[:]
        rds.store.done = True

        args = {
            "symbol_count": len(ds.config["values"]["bytes"]),
            "total_counts": len(cg.store.times)
        }
        y = fn.clock_gen_function(**args)
        cg.store.values = y[:]
        cg.store.done = True

        args = {
            "cl_values": cl.store.values[:],
            "rds_values": rds.store.values[:],
            "cg_values": cg.store.values[:],
            "delta_t": corr.store.times[1] - corr.store.times[0]
        }
        y = fn.correlator_function(**args)
        corr.store.values = y[:]
        corr.store.done = True

    def decisioning(self):
        """"""
        corr = self.store["Corr"]
        ds = self.store["DS"]
        pds = self.store.get("PDS")
        dd = self.store["DD"]

        args = {
            "corr_values": corr.store.values[:],
            "symbol_count": len(ds.config["values"]["bytes"])
        }
        values = fn.decision_device_function(**args)
        counts_per_symbol = len(dd.store.times) // args["symbol_count"]
        y = np.concatenate([np.full(counts_per_symbol, val) for val in values])
        dd.store.values = y[:]
        dd.store.done = True

        pivot_value = pds.config["values"]["pivot_signal_level"] if pds else 0
        bit_arr = []
        for val in values:
            if val > pivot_value:
                bit_arr.append("1")
            elif val < -pivot_value:
                bit_arr.append("0")
            else:
                bit_arr.append("?")
        bits_decoded = "".join(bit_arr)

        dd.config["values"]["received_message"] = bits_decoded


def find_all_blocks_in_system(store, this_block):
    """"""
    store.update({this_block.config["abbr"]: this_block})

    for block in this_block.neighbors:
        if block not in store.values():
            find_all_blocks_in_system(store, block)
