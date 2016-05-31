# input.py

# Defines Input class, contains type, attributes, link to appropriate generator
# function and possible PMF to describe value distribution

import numpy as np
import matplotlib.pyplot as plt

import input_generators

from os.path import join

class Types:
    int          = 1
    float        = 2
    double       = 3
    array        = 4
    uniquearray  = 5
    int_fixed    = 6

    ranged = [ int, float, double ]
    arrays = [ array, uniquearray ]
    fixed  = [ int_fixed ]

class Input:

    def __init__(self, name, type, dist=None, val=None, lower_bound=None,
                 upper_bound=None, size=None, plot_path=None):
        self.name = name
        self.size = size
        self.type = type
        self.val = val
        self.dist = dist
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.plot_path = plot_path

        print self

        # Determine normalization factor and plot pmf for input with value distribution
        if type in Types.ranged:
            self.norm_factor()
            self.plot_pmf()

    def __str__(self):
        if self.type == Types.int:
            return "'{}' (type: int, range: [{}, {}))".format(self.name, self.lower_bound, self.upper_bound)
        elif self.type == Types.float:
            return "'{}' (type: float, range: [{}, {}])".format(self.name, self.lower_bound, self.upper_bound)
        elif self.type == Types.double:
            return "'{}' (type: double, range: [{}, {}])".format(self.name, self.lower_bound, self.upper_bound)
        elif self.type == Types.array:
            return "'{}' (type: array, size: {})".format(self.name, self.size)
        elif self.type == Types.uniquearray:
            return "'{}' (type: uniquearray, size: {})".format(self.name, self.size)
        elif self.type == Types.int_fixed:
            return "'{}' (type: int_fixed)".format(self.name, self.val)

    def generator(self):
        """
        Return reference to generator and arguments: (ref, (arg_1, .. arg_n))
        """
        if self.type == Types.int:
            return (input_generators.gen_int, (self.lower_bound, self.upper_bound))
        if self.type == Types.float:
            return (input_generators.gen_float, (self.lower_bound, self.upper_bound, False))
        if self.type == Types.double:
            return (input_generators.gen_float, (self.lower_bound, self.upper_bound, True))
        elif self.type == Types.array:
            return (input_generators.gen_array, (self.size,))
        elif self.type == Types.uniquearray:
            return (input_generators.gen_uniquearray, (self.size,))
        elif self.type == Types.int_fixed:
            return (input_generators.gen_int_fixed, (self.val,))

    def pmf(self, x, normed=True):
        """
        Combined probability mass function
        """
        if self.type in Types.ranged:

            for lower, upper, (ratio, fun) in self.dist:

                if self.type == Types.float or self.type == Types.double:
                    x = np.float64(x)
                    lower = np.float64(lower)
                    upper = np.float64(upper)

                if x >= lower and x < upper:
                    if normed:
                        return (ratio * fun(x)) * self.norm_fac
                    else:
                        return ratio * fun(x)
            return 0.

        else:
            return 1.

    def norm_factor(self):
        """
        Determine normalization factor for probability mass function
        """
        print "Determining normalization factor for input '{}'...".format(self.name)
        sum = 0
        gen, args = self.generator()
        for val in gen(*args):
            sum += self.pmf(val, normed=False)
        if sum == 0:
            self.norm_fac = 1.
        else:
            self.norm_fac = 1. / sum
        print "Normalization factor: {}".format(self.norm_fac)

    def plot_pmf(self, num=1000):
        """
        Plot probability mass function
        """
        ax = plt.subplot(111)

        if self.type == Types.int:
            x = np.linspace(self.lower_bound, self.upper_bound - 1, num=num, dtype=np.int64)
        elif self.type == Types.float or self.type == Types.double:
            x = np.linspace(self.lower_bound, self.upper_bound, num=num, dtype=np.float64)
        y = [self.pmf(val, normed=True) for val in x]

        ax.set_title("Input value probability distribution {}".format(self))
        ax.set_ylim(0, max(y) + 0.1*(max(y)))
        ax.set_xlim(min(x), max(x) + 0.1*max(x))
        ax.set_xlabel("Input value")
        ax.set_ylabel("Probability")

        plt.plot(x, y, "b.")

        if self.plot_path:
            plt.savefig(join(self.plot_path, "input_{}_pmf.png".format(self.name)))
            print "Value probability distribution saved to '{}'".format(join(self.plot_path, "input_{}_pmf.png".format(self.name)))
