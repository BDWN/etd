# input_generators.py
# Generator functions for various types of input

import numpy as np
import itertools

def gen_combs(gens, pos=0):
    """
    Generate all combinations of generated values, used instead of
    itertools.product to conserve memory

    gens: [ (generator_reference, (arg1, arg2 ... argn), .. ]

    Original by 'Kieran', source:
    http://code.activestate.com/recipes/577415/
    """
    next_gen, comb = None, []
    gen = gens[pos][0](*gens[pos][1])
    while True:
        try:
            yield comb + next_gen.next()
        except (StopIteration, AttributeError):
            comb = [gen.next(),]
            if pos < len(gens) - 1:
                next_gen = gen_combs(gens, pos+1)
            else:
                yield comb

def gen_int(lower_bound, upper_bound):
    """
    Generator for ints from lower to upper bound
    """
    for i in xrange(lower_bound, upper_bound):
        yield i

def gen_float(lower_bound, upper_bound, double=False):
    """
    Generator for single/double precision floats from lower to upper bound
    """
    if double:
        x = np.float64(lower_bound)
    else:
        x = np.float32(lower_bound)
    prev = None
    while x != prev:
        if double:
            yield "{:.2000g}".format(np.float64(x))
        else:
            yield "{:.2000g}".format(np.float32(x))
        prev = x
        if double:
            x = np.nextafter(x, np.float64(upper_bound))
        else:
            x = np.nextafter(x, np.float32(upper_bound))

def gen_array(size):
    """
    Return all combinations for an array with unique values ranging from
    0 to size, returned as comma seperated string
    """
    for comb in itertools.product(range(size), repeat=size):
        yield ",".join(map(str, comb))

def gen_uniquearray(size):
    """
    Returns all permutations for an array with unique values ranging from
    0 to size, returned as comma seperated string
    """
    for perm in itertools.permutations(range(size)):
        yield ",".join(map(str, perm))

def gen_int_fixed(val):
    """
    Return fixed integer
    """
    yield val
