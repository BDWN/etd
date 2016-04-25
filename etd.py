# etd.py
# bladiebla

import numpy as np
import matplotlib.pyplot as plt

from os.path import join

def plot_etd(name, data_file, out_path):

    data = np.genfromtxt(data_file, dtype="int64,float32", delimiter=",",
                         names=["cycles", "frequency"], skip_header=1)

    # Sort and normalize data
    data.sort()
    data["frequency"] /= np.amax(data["frequency"])

    ax = plt.subplot(111)
    ax.set_title("Execution time distribution '{}'".format(name))
    ax.set_xlabel("Execution time (cycles)")
    ax.set_ylabel("Relative frequency")
    ax.set_xlim(min(data["cycles"]), max(data["cycles"]))
    ax.set_ylim(min(data["frequency"]), max(data["frequency"]) + 0.1)

    plt.plot(data["cycles"], data["frequency"], "r-")
    plt.savefig(join(out_path, "{}_frequency.png".format(name)))
    plt.show()

def plot_histogram(name, data_file, out_path):

    data = np.genfromtxt(data_file, dtype=np.int64, skip_header=1)

    ax = plt.subplot(211)
    ax.set_title("Execution time distribution '{}'".format(name))
    ax.set_xlabel("Execution time bin (cycles)")
    ax.set_ylabel("Frequency")
    ax.set_xlim(min(data), max(data))

    plt.hist(data, np.power(len(data), 1/3.0))
    ax = plt.subplot(212)
    ax.set_xlim(min(data), max(data))
    plt.hist(data, 30)
    plt.savefig(join(out_path, "{}_histogram.png".format(name)))

    plt.show()
