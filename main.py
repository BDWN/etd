#!/usr/bin/env python

# main.py
# Runs ETD framework

import argparse
import config
import etd
import multiprocessing

from benchmark import Benchmark
from benchmarks import benchmarks
from os.path import join, isdir

def positive_int(n):
    n = int(n)
    if n < 0:
        raise argparse.ArgumentTypeError("Number of processes must be greater than 0")
    return n

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--overwrite", action="store_true", help="force overwriting of any previous output")
    parser.add_argument("-d", "--debug", action="store_true", help="show compilation and simulator output")
    parser.add_argument("-p", "--processes", type=positive_int, default=8, help="show compilation and simulator output")
    parser.add_argument("bench", type=str, help="name of benchmark")
    args = parser.parse_args()

    if args.bench not in benchmarks:
        print("'{}' benchmark not specified, please select one of the following benchmarks:".format(args.bench))
        for bench_name in benchmarks:
            print(bench_name)
        exit()
    elif not isdir(benchmarks[args.bench]["path"]):
        print("Source directory for benchmark '{}' not found ('{}')".format(args.bench, benchmarks[args.bench]["path"]))
        exit()

    bench = Benchmark(args.bench,
                      benchmarks[args.bench]["input"],
                      args.processes,
                      join(benchmarks[args.bench]["path"]),
                      join(config.main["out_dir"], args.bench),
                      config.gem5["exec"],
                      join(config.gem5["script"]),
                      config.gem5["out_dir"],
                      args.overwrite)

    bench.run(config.gem5["script_args"], debug=args.debug)

    results_dir = join(config.main["out_dir"], args.bench)
    results_filename = "{}.{}".format(config.benchmark["out_file"], config.benchmark["out_ext"])
    results_file = join(results_dir, results_filename)
    etd.plot_etd(results_file, results_dir, name=args.bench, show=False)
