# etd.py
# bladiebla

import numpy as np
import matplotlib.pyplot as plt

from os.path import join

def plot_frequency(name, data_file, out_path):

    data = np.genfromtxt(data_file, dtype=np.int64, skip_header=1)

    cycles, freq = np.unique(data, return_counts=True)

    ax = plt.subplot(111)
    ax.set_title("Execution time distribution '{}'".format(name))
    ax.set_xlabel("Execution time (cycles)")
    ax.set_ylabel("Frequency")

    plt.plot(cycles, freq, "r.")
    plt.savefig(join(out_path, "{}_frequency.png".format(name)))
    plt.show()

def plot_histogram(name, data_file, out_path):

    data = np.genfromtxt(data_file, dtype=np.int64, skip_header=1)

    ax = plt.subplot(211)
    ax.set_title("Execution time distribution '{}'".format(name))
    ax.set_xlabel("Execution time bin (cycles)")
    ax.set_ylabel("Frequency")
    # ax.set_xlim(min(edges), max(edges))

    plt.hist(data, 25)
    ax = plt.subplot(212)
    plt.hist(data, 100)
    plt.savefig(join(out_path, "{}_histogram.png".format(name)))

    plt.show()
