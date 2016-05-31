#!/usr/bin/env python2

# etd.py
# Plotting of execution time distribution

import argparse
import numpy as np
import matplotlib.pyplot as plt

from os.path import join, isfile

def plot_etd(data_file, out_path=None, name=None, show=False):

    if not isfile(data_file):
        print "Error plotting ETD, '{}' not found".format(data_file)

    else:
        try:
            data = np.genfromtxt(data_file, dtype="int64,float32", delimiter=",",
                                 names=["cycles", "frequency"], skip_header=1)
        except:
            print "Error plotting ETD, invalid data file '{}'".format(data_file)
            return

        # Sort and normalize data
        data.sort()
        data["frequency"] /= np.sum(data["frequency"])

        ax = plt.subplot(111)
        if name:
            ax.set_title("Execution time distribution '{}'".format(name))
        else:
            ax.set_title("Execution time distribution")
        ax.set_xlabel("Execution time (cycles)")
        ax.set_ylabel("Probability")
        ax.set_xlim(min(data["cycles"]) - 0.1*(min(data["cycles"])), max(data["cycles"]) + 0.1*(max(data["cycles"])))
        ax.set_ylim(0, max(data["frequency"]) + 0.1*(max(data["frequency"])))

        plt.bar(data["cycles"], data["frequency"], color="blue", lw=2.0)

        if out_path:
            plt.savefig(join(out_path, "{}_etd.png".format(name)))
            print "Execution time distribution plot saved to '{}'".format(join(out_path, "{}_etd.png".format(name)))
        if show:
            plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input csv file (cycles,frequency)")
    args = parser.parse_args()

    plot_etd(args.file, show=True)
