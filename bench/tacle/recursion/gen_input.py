#!/usr/bin/env python

import json
import argparse

from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")

t = Template(
"""
void recursion_init() {
    recursion_input = $i_1;
}
""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate init file")
    parser.add_argument('-i', '--input', type=json.loads)
    args = parser.parse_args()
    f.write(t.substitute(args.input))
    f.close()
