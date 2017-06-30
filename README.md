# EDiFy: An Execution time Distribution Finder
A Python framework for deriving execution time distributions using the [gem5](http://gem5.org) simulator.
The paper in which the framework is introduced can be [found in the ACM digital library](http://dl.acm.org/citation.cfm?id=3062233)

### Requirements
* Python 3
    * Numpy
    * Matplotlib
* [gem5](http://gem5.org)
* Cross compiler for target hardware architecture (e.g. GCC)

### Notes
Please note that this framework has only been tested on Linux, although it should run on other platforms supported by the *gem5* simulator.
As is, the framework is set up to compile and run benchmarks targetting the AARCH64 architecture (64bit ARM).
The framework comes with a set of modified benchmarks taken from the [TACLeBench](http://www.tacle.eu/index.php/activities/taclebench) benchmark suite.

### Installation
Since this framework relies on the *gem5* simulator, please make sure you have it installed and built (a guide can be found on their website).
The required Python modules can either be installed manually via your system package manager, or using `pip`:

`pip install -r requirements.txt`

Install the framework by cloning this repository.

### Configuration
After having successfully installed all required software and downloading the
framework, make sure to adjust the `config.py` file before attempting to
run the framework. This file contains global settings, gem5 configurations and
framework output settings.

### Running the framework
The framework can be run by executing `main.py`. It will run the
simulations, save the results and plot both the input value probability
distributions and the derived execution time distribution.

```
usage: main.py [-h] [-o] [-d] [-p PROCESSES] bench

positional arguments:
  bench                 name of benchmark

optional arguments:
  -h, --help            show this help message and exit
  -o, --overwrite       force overwriting of any previous output
  -d, --debug           show compilation and simulator output
  -p PROCESSES, --processes PROCESSES
                        number of worker processed to spawn
```

# Example benchmark specification
In order for a benchmark to be used by the framework the following points have
to addresses:

* Input variable initializations must be moved to a separate file
* A complementary `gen_input.py` must be created
* A call to `m5_reset_stats()` must be added to the benchmark
* A `Makefile` must be supplied, linking the compiled binary to the gem5 utility library
* The benchmark input specification must be added to `benchmarks.py`

What follows is a short guide on preparing the following benchmark for use with
the framework:

```
int x = some_value; // Input variable
int y = some_value; // Input variable

int main() {
    x = some_value;
    y = some_value;
    int z = 0;
    for (int i = 0; i < x * y; i++) {
        z += i;
    }
    return 0;
}
```

### Detaching input variable initialization
First, make sure the benchmark is contained in its own directory:

`/<path_to_framework>/bench/test_bench`

Now, move the initialization of desired input variables in the source code to a
new file `init.c` and include it in the main source file. Note
that it is not required to assign values to variables in the `init.c`
file since these will be injected by the framework. However, it can be useful
to assign some test values to ensure the program still behaves as expected.

The next step is to include the `m5op.h` file (supplied with the framework in the example benchmarks,
located in the `bench/tacle/<benchmark>/include` directory) and prepend the main benchmark computation
with a call to reset the simulator stats. See the example below:

bench.c:
```
#include "include/m5op.h"
#include "init.c"

int main() {
    benchmark_init();
    m5_reset_stats();
    int z = 0;
    for (int i = 0; i < x * y; i++) {
        z += i;
    }
    m5_exit(0);
    return 0;
}
```

init.c:
```
int x;
int y;

void benchmark_init() {
    x = some_value;
    y = some_value;
}
```

### Creating gen_input.py file
Copy one of the existing `gen_input.py` files from one of the example
benchmarks
directory (`<path_to_framework>/bench/tacle/<bench>/gen_input.py`) to
the `test_bench` directory and supply it the contents of the
`init.c` as follows:

```
#!/usr/bin/env python

import json
import argparse
from os.path import join, dirname, realpath
from string import Template

f = open(join(dirname(realpath(__file__)), "init.c"), "w")
t = Template(
"""
int x;
int y;
void benchmark_init() {
    x = $x;
    y = $y;
}
""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate init file")
    parser.add_argument('-i', '--input', type=json.loads)
    args = parser.parse_args()
    f.write(t.substitute(args.input))
    f.close()
```

Note that `$x` and `$y` are the framework's internal names for the input
variables. They will be used in the input specification to identify the
specific variables. Make sure these are prepended with `$`.

### Makefile
In order for the framework to be able to compile the benchmark, a `Makefile`
must be provided. To facilitate the call to `m5_reset_stats()`, the compiled
binary will have to be linked to the gem5 utility library. See the example
Makefile below:

```
CC=aarch64-linux-gnu-gcc
CFLAGS=-march=armv8-a -static
OBJS=include/m5op_arm_A64.o

all: bench

bench: bench.o
    $(CC) $(CFLAGS) -o a.out bench.o $(OBJS)

bench.o: bench.c
    $(CC) $(CFLAGS) -c bench.c

clean:
    -rm -f *.o
    -rm -f a.out
```

The `m5op.arm.A64.o` file is provided with the framework and can be found in the `bench/tacle/<benchmark>/include` directory.
Note that you can also compile it yourself, the source code is provided in the `<gem5_directory>/util/m5` directory.

### Input specification
After having properly modified the original benchmark source code and setting
up the appropriate `gen_input.py` file, the benchmark input specification must
be added to the `benchmarks.py` file as follows:

```
from input import Types
from distributions import *

benchmarks = {
    ...
    "test_bench" : { "path" : "<path_to_framework>/bench/test_bench/",
                     "input": [
                                   ("x", (Types.int, 1, 20,
                                     [
                                         (1, 10, (2, uniform_dist(1.))),
                                         (10, 20, (1, uniform_dist(1.))),
                                     ])
                                   ),

                                   ("y", (Types.int, 1, 30,
                                     [
                                         (1, 30, (1, uniform_dist(1.))),
                                     ])
                                   ),
                              ]
    },
    ...
}
```

This example input specification defines both `x` and `y` as integer input
types and sets their ranges at `[1,20)` and `[1,30)` respectively. For `y`, the
value probability distribution is uniform. For `x`, a value in the range of
`[1,10)` is deemed twice as likely as a value in the range of `[10,20)`
(specified by the ratio 2:1).

In general, an input specification must adhere to the following format:\\

```
# Input types are defined in input.py
# Distributions are defined in distributions.py

"name" : { "path" : "path_to_benchmark_folder",
           "input": [
                         # Ranged input type
                         (
                           "variable_placeholder_name",
                           (input_type,
                            lower_bound, upper_bound,
                            # Input value distribution
                            [
                                (min_val, max_val, (ratio, dist),
                                (min_val, max_val, (ratio, dist),
                                ...
                                (min_val, max_val, (ratio, dist),
                            ])
                         ),

                         # Array input type
                         (
                           "variable_placeholder_name",
                           (input_type, array_size)
                         ),

                         # Fixed input type
                         (
                           "variable_placeholder_name",
                           (input_type, value)
                         ),

                    ]
}
```
