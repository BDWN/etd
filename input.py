# input.py

# Contains Types class for defining the various type of possible input
# variables to generate. The Input class contains the generator functions to
# go along with the defined input types.

import numpy as np

class Types:

    int32_full = 1          # -(2^31) to 2^31 - 1
    int32_pos  = 2          # 0 to 2^31 - 1
    int32_neg  = 3          # -(2^31) to 0
    int32_uns  = 4          # 0 to 2^32 - 1
    int32_uniquearray = 5   # Unique array permutations, values limited to size

def type_str(input_type):

    if input_type == Types.int32_full:
        return "int32_full"
    elif input_type == Types.int32_pos:
        return "int32_pos"
    elif input_type == Types.int32_neg:
        return "int32_neg"
    elif input_type == Types.int32_uns:
        return "int32_uns"
    elif input_type == Types.int32_uniquearray:
        return "int32_uniquearray"

class Input:

    def __init__(self, input_type):
        self.input_type = input_type

    def gen_input(self):
        if self.input_type == Types.int32_full:
            return self.gen_ints(-np.power(2, 31), np.power(2, 31) - 1)

        elif self.input_type == Types.int32_pos:
            return self.gen_ints(0, np.power(2,31) - 1)

        elif self.input_type == Types.int32_neg:
            return self.gen_ints(-np.power(2, 31), 0)

        elif self.input_type == Types.int32_uns:
            return self.gen_ints(0, np.power(2, 32) - 1)

        elif self.input_type == Types.int32_uniquearray:
            return self.gen_uniquearrays()

    def gen_ints(self, lower, upper):
        # Use xrange to enforce lazy generation as not fill memory
        for i in xrange(lower, upper):
            yield i
