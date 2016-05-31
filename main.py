#!/usr/bin/env python2

# main.py
# Runs ETD framework

import argparse
import config
import etd

from benchmark import Benchmark
from benchmarks import benchmarks
from os.path import join, isdir

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nosim", action="store_true", help="do not run simulations, only plot previous results")
    parser.add_argument("-o", "--overwrite", action="store_true", help="force overwriting of any previous output")
    parser.add_argument("-d", "--debug", action="store_true", help="show compilation and simulator output")
    parser.add_argument("bench", type=str, help="name of benchmark")
    args = parser.parse_args()

    if args.bench not in benchmarks:
        print "'{}' benchmark not specified, please select one of the following benchmarks:".format(args.bench)
        for bench_name in benchmarks:
            print bench_name
        exit()

    if not isdir(benchmarks[args.bench]["path"]):
        print "Source directory for benchmark '{}' not found ('{}')".format(args.bench, benchmarks[args.bench]["path"])
        exit()

    bench = Benchmark(args.bench,
                      benchmarks[args.bench]["input"],
                      join(benchmarks[args.bench]["path"]),
                      join(config.main["out_dir"], args.bench),
                      config.gem5["exec"],
                      join(config.gem5["script"]),
                      config.gem5["out_dir"],
                      args.overwrite)

    if not args.nosim:
        bench.run(config.gem5["script_args"], debug=args.debug)

    results_dir = join(config.main["out_dir"], args.bench)
    results_filename = "{}.{}".format(config.benchmark["out_file"], config.benchmark["out_ext"])
    results_file = join(results_dir, results_filename)
    etd.plot_etd(results_file, results_dir, name=args.bench, show=True)
