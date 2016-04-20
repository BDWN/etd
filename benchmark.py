# benchmark.py
# bladiebla

import json
import subprocess

from shutil import rmtree
from os import mkdir, remove, devnull
from os.path import join, dirname, realpath, isfile

class Benchmark:

    def __init__(self, name, path, out_path, sim_path, sim_script, sim_outdir):
        self.name = name
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

    def run(self, input, sim_flags, debug=False):
        """
        Generate input file for benchmark, compile, run and append execution
        time to output file
        """

        # Show subprocess call output if debug flag is set
        if debug:
            output = None
        else:
            output = open(devnull, "w")

        # Generate input file
        cmd = "{} --input '{}'".format(
                join(self.path, "gen_input.py"),
                json.dumps(input))
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

        return self.extract_cycles()

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
