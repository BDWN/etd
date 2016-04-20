# benchmark.py
# bladiebla

import json
import subprocess
import sys

from input import Input, Types, type_str
from shutil import rmtree
from os import mkdir, remove, devnull
from os.path import join, dirname, realpath, isfile

class Benchmark:

    """Docstring for Benchmark. """

    def __init__(self, name, input, path, out_path, sim_path, sim_script, sim_outdir):
        self.name = name
        self.input = input
        self.path = path
        self.out_path = out_path
        self.sim_path = sim_path
        self.sim_script = sim_script
        self.sim_outdir = sim_outdir

        self.out_file = "cycles.txt"
        self.bench_exec = "a.out"

        # Initialize output directory
        self.clear_output()
        try:
            mkdir(self.out_path)
        except:
            pass
        with open(join(self.out_path, self.out_file), "w") as f:
            f.write("cycles\n")

    def run(self, sim_flags, verbose=False, debug=False):
        """
        Generate input file for benchmark, compile, run and append execution
        time to output file
        """

        # Show subprocess call output if debug flag is set
        if debug:
            output = None
        else:
            output = open(devnull, "w")

        if verbose:
            print "-------------------------"
            print "Running benchmark '{}'".format(self.name)
            for var_name, var_type in self.input:
                print "{} ({})".format(var_name, type_str(var_type))

        for var_name, var_type in self.input:

            # Create generator for input
            var_input = Input(var_type)
            var_gen = var_input.gen_input()

            if verbose:
                print "\n",

            for var_val in var_gen:

                input_json = {var_name:var_val}

                if verbose:
                    sys.stdout.write("\r{}: {}".format(var_name, var_val))
                    sys.stdout.flush()

                # Generate input file
                cmd = "{} --input '{}'".format(
                        join(self.path, "gen_input.py"),
                        json.dumps(input_json))
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

                # Output cycle count
                self.output_cycles(self.extract_cycles())

        if verbose:
            print "\nDone"
            print "-------------------------"

        return True

    def extract_cycles(self):
        """
        Extract cycle count from gem5 stats.txt file
        """

        # Only read first 6 lines, contains all the desired information
        stats = []
        with open(join(self.out_path, self.sim_outdir, "stats.txt"), "r") as f:
            stats.extend(f.readline() for i in range(4))

        # Return tick count
        return stats[3].split()[1]

    def output_cycles(self, ticks):
        """
        Append simulation stats to output file
        """
        with open(join(self.out_path, self.out_file), "a") as f:
            f.write("{}\n".format(ticks))

    def clear_output(self):
        """
        Remove benchmark output directory and contents
        """
        try:
            rmtree(join(self.out_path, self.sim_outdir), ignore_errors=False)
            os.remove(self.out_path, self.out_file)
        except:
            print "Unable to clear output directory for '{}' benchmark, will overwrite existing files".format(self.name)
