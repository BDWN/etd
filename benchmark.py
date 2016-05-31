# benchmark.py
# Defines Benchmark class, handles creation of Input objects, simulation and
# storing of resulting data

import json
import subprocess
import sys
import time
import config

from input import Input, Types
from shutil import rmtree
from os import mkdir, remove, devnull, rename
from os.path import join, dirname, realpath, isfile
from input_generators import gen_combs

class Benchmark:

    def __init__(self, name, input, path, out_path, sim_path, sim_script, sim_outdir, overwrite):
        self.name = name
        self.input = input
        self.path = path
        self.out_path = out_path
        self.sim_path = sim_path
        self.sim_script = sim_script
        self.sim_outdir = sim_outdir
        self.overwrite = overwrite

        self.out_file = config.benchmark["out_file"]
        self.out_ext = config.benchmark["out_ext"]
        self.out_filename = "{}.{}".format(self.out_file, self.out_ext)
        self.bench_exec = config.benchmark["bench_exec"]

        self.results = {}

        print "-------------------------"
        print "Benchmark '{}', {} input variable(s)".format(self.name, len(self.input))

        self.init_inputs()

    def init_inputs(self):
        """
        Consolidate input specification, create Input objects
        """
        self.inputs = []

        print "-------------------------"
        print "Initializing input ".format(self.name)
        print "\n",

        for input_name, input_description in self.input:

            if input_description[0] in Types.ranged:
                input = Input(input_name, input_description[0],
                              lower_bound=input_description[1],
                              upper_bound=input_description[2],
                              dist=input_description[3],
                              plot_path=self.out_path)
                self.inputs.append(input)

            elif input_description[0] in Types.arrays:
                input = Input(input_name, input_description[0], size=input_description[1])
                self.inputs.append(input)

            elif input_description[0] in Types.fixed:
                input = Input(input_name, input_description[0], val=input_description[1])
                self.inputs.append(input)

        print "-------------------------"


    def run(self, script_args, debug=False):
        """
        Generate input file for benchmark, compile, run and store results
        """

        self.init_output()
        sim_count = 0

        # Show subprocess call output if debug flag is set
        if debug:
            output = None
        else:
            output = open(devnull, "w")

        print "-------------------------"
        print "Running benchmark"

        print "\n",

        input_names = [input_var.name for input_var in self.inputs]
        generators = [input_var.generator() for input_var in self.inputs]
        pmfs = [input_var.pmf for input_var in self.inputs]

        # Iterate over all combinations of input values
        for input_vals in gen_combs(generators):

            inputs_dict = dict(zip(input_names, input_vals))

            # Print current input combination
            input_str = ", ".join("{} = {}".format(name, val) for (name, val) in inputs_dict.iteritems())
            sys.stdout.write("\r{}".format(input_str))
            sys.stdout.flush()

            # Generate input file
            cmd = "{} --input '{}'".format(
                    join(self.path, "gen_input.py"),
                    json.dumps(inputs_dict))
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)

            # Compile benchmark with input, requires Makefile
            cmd = "make clean -C {0} && make -C {0}".format(self.path)
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)

            # Run benchmark
            cmd = "{} -q --outdir {} {} -c {} {}".format(
                    self.sim_path,
                    join(self.out_path, self.sim_outdir),
                    join(self.sim_script),
                    join(self.path, self.bench_exec),
                    script_args)
            subprocess.call(cmd, shell=True, stdout=output, stderr=output)
            sim_count = sim_count + 1

            cycles = self.extract_cycles()

            # Determine weight factor, i.e. combined probability, assumes
            # input values are statistically independent
            weight = 1.
            for i in range(len(input_vals)):
                weight *= pmfs[i](input_vals[i])

            # Only store measurement result if probability is bigger than 0.0
            if weight > 0.:
                self.results[cycles] = self.results.get(cycles, 0) + weight

            # Periodically write to output file while running
            if sim_count % 25 == 0:
                self.write_output()

        print "\nDone, ran {} simulations".format(sim_count)
        print "-------------------------\n"

        self.clean_output()
        if self.write_output():
            print "Output saved to '{}'".format(join(self.out_path, self.out_filename))
        else:
            print "Error saving output"

    def extract_cycles(self):
        """
        Extract cycle count from gem5 stats.txt file
        """
        # Only read first 6 lines, contains all the desired information
        stats = []
        with open(join(self.out_path, self.sim_outdir, "stats.txt"), "r") as f:
            stats.extend(f.readline() for i in range(4))
        # Return cycle count
        return stats[3].split()[1]

    def init_output(self):
        """
        Initializate output directory, backup any previous results if directory
        not empty if overwrite flag is not set
        """
        try:
            mkdir(self.out_path)
        except:
            out_file = join(self.out_path, self.out_filename)
            if isfile(out_file):
                if self.overwrite:
                    print "Overwriting previous output file '{}'".format(out_file)
                else:
                    # Rename previous output file, append timestamp
                    new_filename = "{}_{}.{}".format(self.out_file,
                            int(time.time()), self.out_ext)
                    rename(out_file, join(self.out_path, new_filename))
                    print "Backing up previous output file '{}' as '{}'".format(
                            out_file, join(self.out_path, new_filename))

    def write_output(self):
        """
        Write results to file
        """
        with open(join(self.out_path, self.out_filename), "w") as f:
            f.write("cycles,frequency\n")
            for cycles, freq in self.results.items():
                f.write("{},{}\n".format(cycles, freq))
            return True
        return False

    def clean_output(self):
        """
        Remove gem5 simulator output
        """
        try:
            rmtree(join(self.out_path, self.sim_outdir), ignore_errors=False)
        except:
            print "Warning: unable to remove gem5 output directory '{}'".format(join(self.out_path, self.sim_outdir))
