#!/usr/bin/env python

# etd.py
# Plotting of execution time distribution

import argparse
import numpy as np
import matplotlib.pyplot as plt

from os.path import join, isfile

def live_plot_init(name):
    """
    Initializate figure, axes and line objects for live plot
    """
    fig = plt.figure()
    ax = fig.gca()
    line, = ax.plot([],[], "r", linestyle="-")
    ax.set_title("Execution time distribution '{}'".format(name))
    ax.set_xlabel("Execution time (cycles)")
    ax.set_ylabel("Probability")
    return fig, ax, line

def live_plot_update(results, ax, line):
    """
    Update plot dynamically with supplied results
    """
    data = np.fromiter(results.items(),
                       dtype=[("cycles","int64"),("frequency","float32")],
                       count=len(results))
    data.sort()
    data["frequency"] /= np.sum(data["frequency"])
    line.set_data(data["cycles"], data["frequency"])
    ax.set_xlim(min(data["cycles"]) - 0.1*(min(data["cycles"])),
                max(data["cycles"]) + 0.1*(max(data["cycles"])))
    ax.set_ylim(0, max(data["frequency"]) + 0.1*(max(data["frequency"])))
    ax.autoscale_view(True, True, True)

def read_data(data_file):
    """
    Read data from file, sort and normalize
    """
    if not isfile(data_file):
        return None
    else:
        try:
            data = np.genfromtxt(data_file, dtype="int64,float32", delimiter=",",
                                 names=["cycles", "frequency"], skip_header=1)
        except:
            return None
    if data.size > 1:
        data.sort()
    data["frequency"] /= np.sum(data["frequency"])
    return data

def plot_etd(data_file, out_path=None, name=None, show=False):

    data = read_data(data_file)

    if data is None:
        print("Error plotting ETD, unable to read data from '{}'".format(data_file))
        return

    ax = plt.subplot(111)
    if name:
        ax.set_title("Execution time distribution '{}'".format(name))
    else:
        ax.set_title("Execution time distribution")
    ax.set_xlabel("Execution time (cycles)")
    ax.set_ylabel("Probability")
    if data.size > 1:
        ax.set_xlim(min(data["cycles"]) - 0.1*(min(data["cycles"])), max(data["cycles"]) + 0.1*(max(data["cycles"])))
        ax.set_ylim(0, max(data["frequency"]) + 0.1*(max(data["frequency"])))

    bar_width = (max(data["cycles"]) - min(data["cycles"])) / (len(data["cycles"]) * 2.0)
    plt.bar(data["cycles"], data["frequency"], bar_width, color="black", lw=2.0)

    if data.size > 1:
        bcet = min(data["cycles"])
        wcet = max(data["cycles"])
        spread = wcet - bcet
        mean = np.mean(data["cycles"])
        weighted_mean = np.average(data["cycles"], weights=data["frequency"])
        median = np.median(data["cycles"])
        text = "WCET: {:.3g}\nBCET: {:.3g}\n\nMean: {:.3g}\nWeighted mean: {:.3g}\nMedian: {:.3g}\nSpread: {:.3g}".format(wcet, bcet, mean, weighted_mean, median, spread)
        plt.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=12, verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    if out_path:
        plt.savefig(join(out_path, "{}_etd.png".format(name)))
        print("Execution time distribution plot saved to '{}'".format(join(out_path, "{}_etd.png".format(name))))
    if show:
        plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="output file")
    parser.add_argument("out_path", type=str, help="output file")
    parser.add_argument("file", type=str, help="input csv file (cycles,frequency)")
    args = parser.parse_args()

    plot_etd(args.file, name=args.name, out_path=args.out_path, show=True)
