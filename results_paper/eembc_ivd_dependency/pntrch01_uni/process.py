import numpy as np
from os.path import join, isfile

def read_data(data_file, normalize=True):
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
    if normalize:
        data["frequency"] /= np.sum(data["frequency"])
    return data

if __name__ == '__main__':

    print("cycles,frequency")
    for cycles, frequency in read_data("cycles.csv"):
        print("{},{}".format(cycles,frequency))
