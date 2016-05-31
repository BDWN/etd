# benchmarks.py
# Benchmark specifications

# Specification format:
#
# "name" : { "path" : "path_to_benchmark_folder",
#            "input": [
#                          # Ranged input variable specification
#                          (
#                            "variable_placeholder_name",
#                            (input_type,
#                             lower_bound, upper_bound,
#                             # Input value distribution
#                             [
#                                 (min_val, max_val, (ratio, dist),
#                                 (min_val, max_val, (ratio, dist),
#                                 ...
#                                 (min_val, max_val, (ratio, dist),
#                             ])
#                          ),
#
#                          # Array input variable specification
#                          (
#                            "variable_placeholder_name",
#                            (input_type, array_size)
#                          ),
#
#                     ]
# }

from input import Types
from distributions import *

benchmarks = {

    "fac" : { "path" : "bench/fac/",
              "input": [
                            ("i_1", (Types.int, 0, 4,
                             [
                                 (0, 200, (2, gauss_func(100, 30.0, 2))),
                             ])
                            ),
                       ]
    },

    "recursion" : { "path" : "bench/recursion/",
                    "input": [
                                  ("i_1", (Types.int, 0, 200,
                                    [
                                        (0, 100, (1, uniform_dist(1.))),
                                    ])
                                  ),
                             ]
    },

    "prime" : { "path" : "bench/prime/",
                "input": [
                             ("i_1", (Types.int, 0, 50000,
                               [
                                   (0, 50000, (1, uniform_dist(1.))),
                               ])
                             ),
                         ]
    },

    "bsort" : { "path" : "bench/bsort/",
                "input": [
                             ("a_1", (Types.uniquearray, 3)),
                             ("a_1_size", (Types.int_fixed, 3)),
                         ]
    },

    "isort" : { "path" : "bench/insertsort/",
                "input": [
                             ("a_1", (Types.uniquearray, 6)),
                             ("a_1_size", (Types.int_fixed, 6)),
                         ]
    },

}
