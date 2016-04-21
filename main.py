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

benchmarks = {
                "fac"        : [ ("i_1", (Types.int32_pos,))],
                "recursion"  : [ ("i_1", (Types.int32_pos,))],
                "prime"      : [ ("i_1", (Types.int32_uns,))],
                "bsort"      : [ ("a_1", (Types.int32_uniquearray, 6))],
                "insertsort" : [ ("a_1", (Types.int32_uniquearray, 6))]
             }

if __name__ == '__main__':

    sim_flags = "--cpu-type=TimingSimpleCPU"

    bench_name = "bsort"
    bench_input = benchmarks[bench_name]

    bench = Benchmark(bench_name,
                      bench_input,
                      join(config.main["bench_path"], bench_name),
                      join(config.main["out_path"], bench_name),
                      config.gem5["exec"],
                      join(config.gem5["script"]),
                      config.gem5["out_dir"])

    # bench.run(sim_flags, verbose=True)

    etd.plot_frequency(bench_name, "output/{}/cycles.txt".format(bench_name), "output/{}/".format(bench_name))
    etd.plot_histogram(bench_name, "output/{}/cycles.txt".format(bench_name), "output/{}/".format(bench_name))
