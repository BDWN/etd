# input.py

# Contains Types class for defining the various type of possible input
# variables to generate. The Input class contains the generator functions to
# go along with the defined input types.

import itertools
import numpy as np

class Types:
    int          = 1
    uniquearray  = 2

def type_str(input_type):
    if input_type == Types.int:
        return "int"
    elif input_type == Types.uniquearray:
        return "uniquearray"

class Input:

    def __init__(self, input_type, lower_bound=None, upper_bound=None, input_size=None):
        self.input_size = input_size
        self.input_type = input_type
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def gen_input(self):
        if self.input_type == Types.int:
            return self.gen_ints()
        elif self.input_type == Types.uniquearray:
            return self.gen_uniquearrays()

    def gen_ints(self):
        """
        Generator for ints from lower to upper bound
        """
        for i in xrange(self.lower_bound, self.upper_bound+ 1):
            yield i

    def gen_uniquearrays(self):
        """
        Returns all permutations for an array with unique values ranging from
        0 to size, returned as comma seperated string
        """
        for perm in itertools.permutations(range(self.input_size)):
            yield ",".join(map(str, perm))
