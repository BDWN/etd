#!/usr/bin/env python

import json
import argparse

from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")

t = Template(
"""
#define bsort_SIZE $a_1_size

static int bsort_Array[ bsort_SIZE ];

static int bsort_Values[ bsort_SIZE ] = { $i_1, $i_2, $i_3, $i_4, $i_5, $i_6 };

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
