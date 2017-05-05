# benchmark.py
# Defines Benchmark class, handles creation of Input objects, simulation and
# storing of resulting data

import json
import subprocess
import sys
import time
import config
import multiprocessing
import os
import os.path
import shutil
import matplotlib.pyplot as plt
import numpy as np
import warnings
import etd
import math

from input import Input, Types
from input_generators import gen_combs

class Benchmark:

    def __init__(self, name, input, n_proc, path, out_path, sim_path, sim_script, sim_outdir, overwrite):

        warnings.simplefilter("ignore")

        self.name = name
        self.input = input
        self.n_proc = n_proc
        self.path = path
        self.out_path = out_path
        self.sim_path = sim_path
        self.sim_script = sim_script
        self.sim_outdir = sim_outdir
        self.overwrite = overwrite

        self.largest = None

        self.tmp_dir = config.benchmark["copy_prefix"] + self.name

        self.out_file = config.benchmark["out_file"]
        self.out_ext = config.benchmark["out_ext"]
        self.out_filename = "{}.{}".format(self.out_file, self.out_ext)
        self.bench_exec = config.benchmark["bench_exec"]

        self.queue = multiprocessing.Queue()
        self.results = {}
        self.counter = multiprocessing.Value('i', 0)

        print("-------------------------\n")
        print("Benchmark '{}', {} input variable(s)".format(self.name, len(self.input)))

        self.init_output()
        self.largest_range()
        self.init_input()
        self.divide_input()

    def init_input(self):
        """
        Initialize undivided inputs, PMF of undivided input is required
        """
        print("\n-------------------------\n")
        print("Initializing input \n".format(self.name))

        self.inputs = []

        for input_name, input_description in self.input:

            if input_description[0] in Types.ranged:
                input = Input(input_name, input_description[0],
                              lower_bound=input_description[1],
                              upper_bound=input_description[2],
                              dist=input_description[3],
                              plot_path=self.out_path,
                              debug=True)
                self.inputs.append(input)

            elif input_description[0] in Types.arrays:
                input = Input(input_name, input_description[0],
                              size=input_description[1], prob=1.0, debug=True)
                self.inputs.append(input)

            elif input_description[0] in Types.fixed:
                input = Input(input_name, input_description[0],
                              val=input_description[1], prob=1.0, debug=True)
                self.inputs.append(input)

            elif input_description[0] is Types.bool:
                input = Input(input_name, input_description[0],
                              true_prob=input_description[1],
                              false_prob=input_description[2], debug=True)
                self.inputs.append(input)

            elif input_description[0] is Types.int_array_unique:
                input = Input(input_name, input_description[0],
                              size=input_description[1], lower_bound=0,
                              upper_bound=math.factorial(input_description[1]),
                              prob=1.0, debug=True)
                self.inputs.append(input)

        print("\n-------------------------\n")

    def init_working_dirs(self):
        """
        Create temporary working directories for workers, copies benchmark
        source code to seperate directories
        """
        tmp_dirname = config.benchmark["copy_prefix"] + self.name
        try:
            # Create temp directory
            if os.path.exists(os.path.join(self.path, self.tmp_dir)):
                shutil.rmtree(os.path.join(self.path, self.tmp_dir))
            self.bench_files = os.listdir(self.path)
            os.mkdir(os.path.join(self.path, self.tmp_dir))
            # Copy benchmark source files to working directories
            for i in range(self.n_proc):
                os.mkdir(os.path.join(self.path, self.tmp_dir, str(i)))
                for item in self.bench_files:
                    source = os.path.join(self.path, item)
                    dest = os.path.join(self.path, self.tmp_dir, str(i), item)
                    if os.path.isdir(source):
                        shutil.copytree(source, dest)
                    else:
                        shutil.copy(source, dest)
            return True
        except:
            return False

    def init_output(self):
        """
        Initializate output directory, backup any previous results if directory
        not empty if overwrite flag is not set
        """
        try:
            os.makedirs(self.out_path)
        except:
            out_file = os.path.join(self.out_path, self.out_filename)
            if os.path.isfile(out_file):
                if self.overwrite:
                    print("Overwriting previous output file '{}'".format(out_file))
                else:
                    # Rename previous output file, append timestamp
                    new_filename = "{}_{}.{}".format(self.out_file,
                            int(time.time()), self.out_ext)
                    os.rename(out_file, os.path.join(self.out_path, new_filename))
                    print("Backing up previous output file '{}' as '{}'".format(
                            out_file, os.path.join(self.out_path, new_filename)))

    def write_output(self):
        """
        Write results to file
        """
        with open(os.path.join(self.out_path, self.out_filename), "w") as f:
            f.write("cycles,frequency\n")
            for cycles, freq in self.results.items():
                f.write("{},{}\n".format(cycles, freq))
            return True
        return False

    def clean_output(self):
        """
        Remove gem5 simulator output files and temporary working directories
        """
        try:
            shutil.rmtree(os.path.join(self.out_path, self.sim_outdir))
            shutil.rmtree(os.path.join(self.path, self.tmp_dir))
            return True
        except:
            return False

    def extract_cycles(self, n):
        """
        Extract cycle count from gem5 stats.txt file, n is the process number
        dictating in what directory to find the stats.txt file
        """
        stats = []
        with open(os.path.join(self.out_path, self.sim_outdir, str(n), "stats.txt"), "r") as f:
            stats.extend(f.readline() for i in range(4))
        return stats[3].split()[1]

    def largest_range(self):
        """
        Determine index of input variable with largest range, limit n_proc to
        this range if it is less than the specified n_proc
        """
        ranges = []
        for i, (_, input_description) in enumerate(self.input):
            if input_description[0] is Types.int:
                ranges.append((i, input_description[2] - input_description[1]))
            elif input_description[0] is Types.bool:
                ranges.append((i, 2))
            elif input_description[0] is Types.int_array_unique:
                ranges.append((i, math.factorial(input_description[1])))

        if ranges:
            largest = None
            for i, range in ranges:
                if largest:
                    if range > largest[1]:
                        largest = (i, range)
                else:
                    largest = (i, range)
            self.n_proc = min(largest[1], self.n_proc)
            self.largest = largest
        else:
            self.n_proc = 1

        print("Number of processes: {} (limited by largest range)".format(self.n_proc))

    def divide_input(self):
        """
        Divide input over worker processes, create Input objects
        """

        self.divided_input = [[] for _ in range(self.n_proc)]

        # TODO iterate over self.inputs not self.input, input objects

        for idx, (input_name, input_description) in enumerate(self.input):

            if input_description[0] in Types.fixed:
                for i in range(self.n_proc):
                    input = Input(input_name, input_description[0],
                                  val=input_description[1], prob=1.0)
                    self.divided_input[i].append(input)

            elif input_description[0] in Types.arrays:
                for i in range(self.n_proc):
                    input = Input(input_name, input_description[0],
                                  size=input_description[1], prob=1.0)
                    self.divided_input[i].append(input)

            elif input_description[0] is Types.bool:
                if idx is self.largest[0] and self.n_proc == 2:
                    # Divide boolean values over 2 processes
                    input = Input(input_name, Types.bool_fixed, val=True, prob=input_description[1])
                    self.divided_input[0].append(input)
                    input = Input(input_name, Types.bool_fixed, val=False, prob=input_description[2])
                    self.divided_input[1].append(input)
                else:
                    for i in range(self.n_proc):
                        input = Input(input_name, input_description[0],
                                      true_prob=input_description[1],
                                      false_prob=input_description[2])
                        self.divided_input[i].append(input)

            elif input_description[0] is Types.int:

                # Only divide a single input (with the largest range) over workers
                if idx is self.largest[0]:
                    min_val = input_description[1]
                    max_val = input_description[2]
                    num_range = max_val - min_val
                    num_subrange = num_range // self.n_proc
                    for i in range(self.n_proc):
                        lower = min_val + (i * num_subrange)
                        if i is not self.n_proc - 1:
                            upper = min_val + (i+1) * num_subrange
                        else:
                            # Last process gets remainder
                            upper = max_val
                        input = Input(input_name, input_description[0],
                                      lower_bound=lower,
                                      upper_bound=upper,
                                      dist=input_description[3])
                        self.divided_input[i].append(input)
                else:
                    for i in range(self.n_proc):
                        input = Input(input_name, input_description[0],
                                      lower_bound=input_description[1],
                                      upper_bound=input_description[2],
                                      dist=input_description[3])
                        self.divided_input[i].append(input)

            elif input_description[0] is Types.int_array_unique:

                if idx is self.largest[0]:
                    min_val = 0
                    max_val = math.factorial(input_description[1])
                    num_range = max_val - min_val
                    num_subrange = num_range // self.n_proc
                    for i in range(self.n_proc):
                        lower = min_val + (i * num_subrange)
                        if i is not self.n_proc - 1:
                            upper = min_val + (i+1) * num_subrange
                        else:
                            upper = max_val
                        input = Input(input_name, input_description[0],
                                      size=input_description[1],
                                      lower_bound=lower, upper_bound=upper,
                                      prob=1.0, debug=True)
                        self.divided_input[i].append(input)
                else:
                    for i in range(self.n_proc):
                        input = Input(input_name, input_description[0],
                                      size=input_description[1], lower_bound=0,
                                      upper_bound=math.factorial(input_description[1]),
                                      prob=1.0, debug=True)
                        self.divided_input[i].append(input)

    def output_worker(self):
        """
        Store measurements from queue into results dict, periodically write
        results to output file and update live plot
        """
        plt.close()
        fig, ax, line = etd.live_plot_init(self.name)
        fig.show()

        while True:
            item = self.queue.get()
            if item == "DONE":
                if not self.write_output():
                    print("Warning: unable to write to output file")
                plt.close('all')
                break
            else:
                self.counter.value += 1
                self.results[item[0]] = self.results.get(item[0], 0) + item[1]
                if self.counter.value % config.benchmark["write_interval"] == 0:
                    if not self.write_output():
                        print("Warning: unable to write to output file")
                if self.counter.value % config.benchmark["plot_interval"] == 0:
                    etd.live_plot_update(self.results, ax, line)
                    plt.pause(0.1)

    def measurement_worker(self, n, inputs, output, script_args):
        """
        Iterate over combinations of input values, generates input file,
        compiles benchmark, runs benchmark and saves execution time
        """
        input_names = [input_obj.name for input_obj in inputs]
        generators = [input_obj.generator() for input_obj in inputs]
        # Obtain PMF from undivided input
        pmfs = [input_obj.pmf for input_obj in self.inputs]

        # Iterate over all combinations of input values
        for input_vals in gen_combs(generators):

            # Determine weight factor, i.e. combined probability, assumes
            # input values are statistically independent
            weight = 1.
            for i in range(len(input_vals)):
                weight *= pmfs[i](input_vals[i])

            # Do not simulate 0 probability input
            if weight == 0:
                continue

            inputs_dict = dict(zip(input_names, input_vals))

            # Print current input combination
            input_str = ", ".join("{} = {}".format(name, val) for (name, val) in inputs_dict.items())
            # sys.stdout.write("{}\r".format(input_str))
            # sys.stdout.flush()
            sys.stdout.write("Worker {}: {}\n".format(n, input_str))

            # Generate input file
            cmd = "{} --input '{}'".format(
                    os.path.join(self.path, self.tmp_dir, str(n), "gen_input.py"),
                    json.dumps(inputs_dict))
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)

            # Compile benchmark with input, requires Makefile
            cmd = "make clean -C {0} && make -C {0}".format(os.path.join(self.path, self.tmp_dir, str(n)))
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)

            # Run benchmark
            cmd = "{} -q --outdir {} {} -c {} {}".format(
                    self.sim_path,
                    os.path.join(self.out_path, self.sim_outdir, str(n)),
                    os.path.join(self.sim_script),
                    os.path.join(self.path, self.tmp_dir, str(n), self.bench_exec),
                    script_args)
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)

            cycles = self.extract_cycles(n)

            self.queue.put((cycles, weight))

    def run(self, script_args, debug=False):
        """
        Generate input file for benchmark, compile, run and store results
        """
        # Show subprocess call output if debug flag is set
        if debug:
            output = None
        else:
            output = open(os.devnull, "w")

        print("-------------------------\n")
        print("Running benchmark\n")

        if not self.init_working_dirs():
            print("Warning: unable to create temporary working directories")
            exit()

        output_process = multiprocessing.Process(target=self.output_worker)
        workers = [multiprocessing.Process(target=self.measurement_worker,
                                           args=(i, self.divided_input[i],
                                                 output, script_args))
                   for i in range(self.n_proc)]

        output_process.start()
        for w in workers:
            w.start()

        for w in workers:
            w.join()

        # Notify output worker that the measurements have finished
        self.queue.put("DONE")
        output_process.join()

        print("\nDone, ran {} simulations".format(self.counter.value))
        print("Output saved to '{}'".format(os.path.join(self.out_path, self.out_filename)))
        print("\n-------------------------\n")

        if not self.clean_output():
            print("Warning: unable to remove temporary output files and working directories")
