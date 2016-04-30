# etd.py
# Plotting execution time distribution

import numpy as np
import matplotlib.pyplot as plt

from os.path import join

def plot_etd(name, data_file, out_path):

    data = np.genfromtxt(data_file, dtype="int64,float32", delimiter=",",
                         names=["cycles", "frequency"], skip_header=1)

    # Sort and normalize data (divide by total number of measurements)
    data.sort()
    num_measurements = np.sum(data["frequency"])
    data["frequency"] /= num_measurements

    ax = plt.subplot(111)
    ax.set_title("Execution time distribution '{}' ({} measurements)".format(name, int(num_measurements)))
    ax.set_xlabel("Execution time (cycles)")
    ax.set_ylabel("Relative frequency")
    ax.set_xlim(min(data["cycles"]), max(data["cycles"]))
    ax.set_ylim(0, max(data["frequency"]) + 0.1*(max(data["frequency"])))

    plt.plot(data["cycles"], data["frequency"], color="red", lw=2.0)
    plt.savefig(join(out_path, "{}_etd.png".format(name)))
    plt.show()
