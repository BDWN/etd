#!/usr/bin/env python2

import json
import argparse

from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")

t = Template(
"""
#define bsort_SIZE $size

static int bsort_Array[ bsort_SIZE ];

static int bsort_Values[ bsort_SIZE ] = { $a_1 };

void bsort_init( void ) {
    for (int i = 0; i < bsort_SIZE; i++) {
        bsort_Array[i] = bsort_Values[i];
    }
}
""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate init file")
    parser.add_argument('-i', '--input', type=json.loads)
    args = parser.parse_args()
    f.write(t.substitute(args.input))
    f.close()
