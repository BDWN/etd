# input_generators.py
# Generator functions for various types of input

import numpy as np
import math
import itertools

def iround(x):
    return int(round(x) - .5) + (x > 0)

def tr(i_min, i_max):
    """
    Traversal function, attempts to evenly traverse [i_min, i_max) by always
    hitting the middle of the univisited space
    """
    if i_max - i_min == 1:
        yield i_min
        raise StopIteration

    # Yield corner cases first
    yield i_min
    yield i_max - 1

    n = i_max - i_min - 1

    for i in range(1, 2**(math.ceil(math.log(n,2)))):
        logValue = np.floor(np.log2(i))
        expValue = 2**(logValue)
        expValueInc = 2**(logValue + 1)
        offset = 1.0/expValueInc
        step = (i - expValue)/expValue
        factor = offset + step
        range2N = 2**(np.ceil(np.log2(n)))
        aux = iround(range2N*factor)
        if (aux <= n - 1):
            yield int(i_min + aux)

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
            yield comb + next_gen.__next__()
        except (StopIteration, AttributeError):
            comb = [gen.__next__(),]
            if pos < len(gens) - 1:
                next_gen = gen_combs(gens, pos+1)
            else:
                yield comb

def gen_int(lower_bound, upper_bound):
    """
    Generator for ints from lower to upper bound
    """
    for i in range(lower_bound, upper_bound):
        yield i

def gen_int_tr(lower_bound, upper_bound):
    """
    Generator for int from lower to upper bound, implements traversal function
    to generate better coverage
    """
    return tr(lower_bound, upper_bound)

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

def gen_bool():
    """
    Return boolean values
    """
    yield "true"
    yield "false"

def gen_bool_fixed(val):
    """
    Return fixed boolean
    """
    if val:
        yield "true"
    else:
        yield "false"

def gen_int_array_unique(size, i_min, i_max):
    """
    Returns all permutations for an array with unique values ranging from
    0 to size, returned as comma seperated string
    """
    for i in tr(i_min, i_max):
        arrayList = []
        arrayList.extend(range(0,size))
        resultList = []
        rMax = math.factorial(size)
        counter = size
        while (counter > 0 and i < rMax):
            divFactor = math.factorial(counter-1)
            (div, mod) = divmod(i,divFactor)
            i = mod
            newElement = arrayList[div]
            resultList.append(newElement)
            arrayList = arrayList[:div] + arrayList[div+1 :]
            counter = counter - 1
        yield ",".join(map(str, resultList))
