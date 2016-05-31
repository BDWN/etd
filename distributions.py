# distributions.py

# Input distributions

import math
import numpy as np

def uniform_dist(p):
    """
    Return fixed probability (i.e. constant)
    """
    def uniform_dist(x):
        return p
    return uniform_dist

def gauss_func(mu, sig, height, y_offset=0.):
    """
    Return gauss function
    """
    def gauss_func(x):
        return y_offset + height * np.exp(-1. * ( (x - mu)**2 / (2. * sig**2) ))
    return gauss_func

def normal_dist(mu, sig, y_offset=0.):
    """
    Return probability density function for normal distribution
    """
    return gauss_func(mu, sig, 1. / (sig * np.sqrt(2. * np.pi)), y_offset)
