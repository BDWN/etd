#!/usr/bin/env python2

# main.py
# bladiebla

import subprocess
import argparse
import re

import config
import etd

from input import Types
from benchmark import Benchmark

from os.path import join

if __name__ == '__main__':

    # name = "fac"
    # fac = Benchmark(name,
    #                 join(config.main["bench_path"], name),
    #                 join(config.main["out_path"], name),
    #                 config.gem5["exec"],
    #                 join(config.gem5["script"]),
    #                 config.gem5["out_dir"])
    #
    # for i in range(0, 500):
    #     ticks = fac.run({"v_1":i}, "--cpu-type=TimingSimpleCPU")
    #     fac.output_cycles(ticks)

    name = "prime"
    input = [ ("v_1", Types.int32_pos), ("v_1", Types.int32_pos) ]
    bench = Benchmark(name,
                      input,
                      join(config.main["bench_path"], name),
                      join(config.main["out_path"], name),
                      config.gem5["exec"],
                      join(config.gem5["script"]),
                      config.gem5["out_dir"])

    bench.run("--cpu-type=TimingSimpleCPU", verbose=True)

    # etd.plot_frequency("prime", "output/prime/cycles.txt", "output/prime/")
    # etd.plot_histogram("prime", "output/prime/cycles.txt", "output/prime/")
