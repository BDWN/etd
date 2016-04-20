#!/usr/bin/env python2

import json
import argparse

from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")

t = Template(
"""
void fac_init()
{
    fac_s = 0;
    fac_n = $v_1;
}
""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate init file")
    parser.add_argument('-i', '--input', type=json.loads)
    args = parser.parse_args()
    f.write(t.substitute(args.input))
    f.close()
