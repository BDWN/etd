# benchmark.py
# bladiebla

import json
import subprocess
import sys
import time

import config

from input import Input, Types, type_str
from shutil import rmtree
from os import mkdir, remove, devnull, rename
from os.path import join, dirname, realpath, isfile

class Benchmark:

    """Docstring for Benchmark. """

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

    def run(self, sim_flags, debug=False):
        """
        Generate input file for benchmark, compile, run and append execution
        time to output file
        """

        self.init_output()

        sim_count = 0

        # Show subprocess call output if debug flag is set
        if debug:
            output = None
        else:
            output = open(devnull, "w")

        print "-------------------------"
        print "Running benchmark '{}'".format(self.name)
        for input_name, input_type in self.input:
            print "{} ({})".format(input_name, type_str(input_type[0]))

        for input_name, input_description in self.input:
            # Create generator for input, input_description tuple:
            # int:          (Types.int, lower_bound, upper_bound)
            # uniquearray:  (Types.uniquearray, size)
            input_type = input_description[0]
            if input_type == Types.int:
                input = Input(input_type, lower_bound=input_description[1],
                                                    upper_bound=input_description[2])
            elif input_type == Types.uniquearray or input_type == Types.array:
                input = Input(input_type, input_size=input_description[1])
            input_gen = input.gen_input()

            print "\n",

            # Loop over generated input values
            for input_val in input_gen:

                # Construct command line argument for gen_input.py
                input_arg = {input_name:input_val}
                if input_type == Types.uniquearray or input_type == Types.array:
                    input_arg["size"] = input_description[1]

                sys.stdout.write("\r{}: {}".format(input_name, input_val))
                sys.stdout.flush()

                # Generate input file
                cmd = "{} --input '{}'".format(
                        join(self.path, "gen_input.py"),
                        json.dumps(input_arg))
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
                        sim_flags)
                subprocess.call(cmd, shell=True, stdout=output, stderr=output)
                sim_count = sim_count + 1

                cycles = self.extract_cycles()
                self.results[cycles] = self.results.get(cycles, 0) + 1

                # Periodically write to output file while running
                if sim_count % 25 == 0:
                    self.write_output()

        print "\nDone, ran {} simulations".format(sim_count)
        print "-------------------------"

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
                    new_filename = "{}_{}.{}".format(self.out_file, int(time.time()), self.out_ext)
                    rename(out_file, join(self.out_path, new_filename))
                    print "Backing up previous output file '{}' as '{}'".format(out_file, join(self.out_path, new_filename))

    def clean_output(self):
        """
        Remove gem5 simulator output
        """
        try:
            rmtree(join(self.out_path, self.sim_outdir), ignore_errors=False)
        except:
            print "Warning: unable to remove gem5 output directory '{}'".format(join(self.out_path, self.sim_outdir))
