#!/usr/bin/env python2

# main.py
# bladiebla

import argparse

import config
import etd

from benchmark import Benchmark
from benchmarks import benchmarks

from os.path import join

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nosim", action="store_true", help="do not perform benchmarks, only plot results")
    parser.add_argument("-o", "--overwrite", action="store_true", help="force overwriting of any previous output")
    parser.add_argument("-d", "--debug", action="store_true", help="show compilation and simulator output")
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
                      config.gem5["out_dir"],
                      args.overwrite)

    if not args.nosim:
        bench.run(config.gem5["script_args"], debug=args.debug)

    etd.plot_etd("output/{}/cycles.csv".format(args.bench), out_path="output/{}/".format(args.bench), name=args.bench, show=True)
