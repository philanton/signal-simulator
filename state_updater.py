import matplotlib.pyplot as plt

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
        for block in self.store.values():
            block.store.done = False

        find_all_blocks_in_system(self.store, block)
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

        # for block in self.store.values():
        #     plt.plot(block.store.times, block.store.values)
        # plt.show()

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
        rds = self.store["RDS"]
        cl = self.store["CL"]
        corr = self.store["Corr"]

        rds.store.values = self.store["DS"].store.values[:]
        rds.store.done = True

        args = {
            "cl_values": cl.store.values[:],
            "rds_values": rds.store.values[:],
            "delta_t": corr.store.times[1] - corr.store.times[0]
        }
        y = fn.correlator_function(**args)
        corr.store.values = y[:]
        corr.store.done = True

    def decisioning(self):
        """"""
        pass


def find_all_blocks_in_system(store, this_block):
    """"""
    store.update({this_block.config["abbr"]: this_block})

    neighbor_abbrs = [block.config["abbr"] for block in this_block.neighbors]
    dependencies = set(this_block.config["depends"])
    this_block.store.done = dependencies.issubset(neighbor_abbrs)

    for block in this_block.neighbors:
        if block not in store.values():
            find_all_blocks_in_system(store, block)
