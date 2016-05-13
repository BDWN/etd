#!/usr/bin/env python2

import json
import argparse

from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")

t = Template(
"""
#define ARRAY_SIZE $a_1_size

unsigned int insertsort_a[ARRAY_SIZE];

void insertsort_initialize(unsigned int* array) {
    register int i;
    for ( int i = 0; i < ARRAY_SIZE; i++ )
        insertsort_a[i] = array[i];
}

void insertsort_init() {
    unsigned int a[ARRAY_SIZE] = { $a_1 };
    insertsort_initialize(a);
}
""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate init file")
    parser.add_argument('-i', '--input', type=json.loads)
    args = parser.parse_args()
    f.write(t.substitute(args.input))
    f.close()
