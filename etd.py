#!/usr/bin/env python2

# etd.py
# Plotting of execution time distribution

import argparse
import numpy as np
import matplotlib.pyplot as plt

from os.path import join, isfile

def plot_etd(data_file, out_path=None, name=None, show=False):

    if not isfile(data_file):
        print "File '{}' not found".format(data_file)

    else:
        try:
            data = np.genfromtxt(data_file, dtype="int64,float32", delimiter=",",
                                 names=["cycles", "frequency"], skip_header=1)
        except:
            print "Invalid data file '{}'".format(data_file)
            return

        # Sort and normalize data (divide by total number of measurements)
        data.sort()
        num_measurements = np.sum(data["frequency"])
        data["frequency"] /= num_measurements

        ax = plt.subplot(111)
        if name:
            ax.set_title("Execution time distribution '{}' ({} measurements)".format(name, int(num_measurements)))
        else:
            ax.set_title("Execution time distribution ({} measurements)".format(int(num_measurements)))
        ax.set_xlabel("Execution time (cycles)")
        ax.set_ylabel("Relative frequency")
        ax.set_xlim(min(data["cycles"]) - 0.1*(min(data["cycles"])), max(data["cycles"]) + 0.1*(max(data["cycles"])))
        ax.set_ylim(0, max(data["frequency"]) + 0.1*(max(data["frequency"])))

        # plt.plot(data["cycles"], data["frequency"], color="black", lw=1.0)
        # plt.fill_between(data["cycles"],data["frequency"], color="grey")
        plt.bar(data["cycles"], data["frequency"], color="blue", lw=2.0)
        if out_path:
            plt.savefig(join(out_path, "etd.png".format(name)))
            print "Execution time distribution plot saved to '{}'".format(join(out_path, "{}_etd.png".format(name)))
        if show:
            plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input csv file (cycles,frequency)")
    args = parser.parse_args()

    plot_etd(args.file, show=True)
