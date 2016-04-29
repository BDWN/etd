#!/usr/bin/env python2

# main.py
# bladiebla

import argparse

import config
import etd

from input import Types
from benchmark import Benchmark

from os.path import join

benchmarks = {
                "fac"        : [ ("i_1", (Types.int, 90, 100))],
                "recursion"  : [ ("i_1", (Types.int, 0, 25))],
                "prime"      : [ ("i_1", (Types.int, 0, 100))],
                "bsort"      : [ ("a_1", (Types.uniquearray, 7))],
                "insertsort" : [ ("a_1", (Types.uniquearray, 7))]
             }

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress summary output")
    parser.add_argument("-d", "--debug", action="store_true", help="show command output")
    parser.add_argument("bench", type=str, help="name of benchmark")
    args = parser.parse_args()

    if args.bench not in benchmarks:
        print "'{}' benchmark not implemented, please select one of the following benchmarks:".format(args.bench)
        for bench_name in benchmarks:
            print bench_name

    bench_input = benchmarks[args.bench]

    bench = Benchmark(args.bench,
                      bench_input,
                      join(config.main["bench_path"], args.bench),
                      join(config.main["out_path"], args.bench),
                      config.gem5["exec"],
                      join(config.gem5["script"]),
                      config.gem5["out_dir"])

    bench.run(config.gem5["sim_flags"], quiet=args.quiet, debug=args.debug)

    etd.plot_etd(args.bench, "output/{}/cycles.txt".format(args.bench), "output/{}/".format(args.bench))
