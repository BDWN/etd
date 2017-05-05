# benchmarks.py
# Benchmark input specifications

# Input types are defined in input.py
# Distributions are defined in distributions.py
#
# Specification format:
#
# "name" : { "path" : "path_to_benchmark_folder",
#            "input": [
#                          # Ranged input type
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
#                          # Array input type
#                          (
#                            "variable_placeholder_name",
#                            (input_type, array_size)
#                          ),
#
#                          # Fixed input type
#                          (
#                            "variable_placeholder_name",
#                            (input_type, value)
#                          ),
#
#                     ]
# }


from input import Types
from distributions import *

benchmarks = {

    "bsort" : { "path" : "bench/tacle/bsort/",
                 "input": [
                             ("i_1", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_2", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_3", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_4", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_5", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_6", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("a_1_size", (Types.int_fixed, 6)),
                          ]
    },

    "bsort2" : { "path" : "bench/tacle/bsort2/",
                 "input": [
                             ("a_1", (Types.int_array_unique, 8)),
                             ("a_1_size", (Types.int_fixed, 8)),
                          ]
    },

    "bsort3" : { "path" : "bench/tacle/bsort2/",
                 "input": [
                             ("a_1", (Types.uniquearray, 6)),
                             ("a_1_size", (Types.int_fixed, 6)),
                          ]
    },

    "bitmnp01" : { "path" : "bench/eembc/bitmnp01/",
                   "input": [
                                 ("i_1", (Types.int, 0, 2**9,
                                  [
                                      (0, 2**16, (1, uniform_dist(1.))),
                                  ])
                                 ),
                                 ("i_2", (Types.int, 0, 2,
                                  [
                                      (0, 2**16, (1, uniform_dist(1.))),
                                  ])
                                 ),
                            ]
    },

    "bitmnp01normal" : { "path" : "bench/eembc/bitmnp01normal/",
                   "input": [
                                 ("i_1", (Types.int, 0, 2**9,
                                  [
                                      (0, 2**32, (1, gauss_func(256, 64.0, 7))),
                                  ])
                                 ),
                                 ("i_2", (Types.int, 0, 2,
                                  [
                                      (0, 2**16, (1, uniform_dist(1.))),
                                  ])
                                 ),
                            ]
    },

    "tblook01" : { "path" : "bench/eembc/tblook01/",
                   "input": [
                                 ("i_1", (Types.int, 0, 512,
                                  [
                                      (0, 1024, (1, uniform_dist(1.))),
                                  ])
                                 ),
                                 ("i_2", (Types.int, 0, 512,
                                  [
                                      (0, 1024, (1, uniform_dist(1.))),
                                  ])
                                 ),
                            ]
    },

    "tblook01normal" : { "path" : "bench/eembc/tblook01normal/",
                   "input": [
                                 ("i_1", (Types.int, 0, 512,
                                  [
                                      (0, 2**32, (1, gauss_func(256, 64.0, 7))),
                                  ])
                                 ),
                                 ("i_2", (Types.int, 0, 512,
                                  [
                                      (0, 2**32, (1, gauss_func(256, 64.0, 7))),
                                  ])
                                 ),
                            ]
    },

    "pntrch01" : { "path" : "bench/eembc/pntrch01/",
                   "input": [
                                 ("i_1", (Types.int, 0, 2**8,
                                  [
                                      (-2**16, 2**16, (1, uniform_dist(1.))),
                                  ])
                                 ),
                            ]
    },

    "pntrch01normal" : { "path" : "bench/eembc/pntrch01/",
                   "input": [
                                 ("i_1", (Types.int, 0, 2**8,
                                  [
                                      (0, 2**32, (1, gauss_func(128, 32.0, 7))),
                                  ])
                                 ),
                            ]
    },

    "fac" : { "path" : "bench/tacle/fac/",
              "input": [
                            ("i_1", (Types.int, 0, 20,
                             [
                                 (0, 2**32, (2, gauss_func(2**7+80, 15.0, 7))),
                             ])
                            ),
                       ]
    },

    "recursion" : { "path" : "bench/tacle/recursion/",
                    "input": [
                                  ("i_1", (Types.int, 0, 2**8,
                                    [
                                        (0, 50, (1, uniform_dist(1.))),
                                        (50, 2**8, (1, uniform_dist(1.))),
                                    ])
                                  ),
                             ]
    },

    "prime" : { "path" : "bench/tacle/prime/",
                "input": [
                             ("i_1", (Types.int, 0, 512,
                               [
                                   (0, 512, (1, uniform_dist(1.))),
                                   (512, 1024, (1, uniform_dist(1.))),
                               ])
                             ),
                         ]
    },

    "isort" : { "path" : "bench/tacle/insertsort/",
                "input": [
                             ("i_1", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_2", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_3", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("i_4", (Types.int, 0, 2**2, [(0, 2**2, (1, uniform_dist(1.))),])),
                             ("a_1_size", (Types.int_fixed, 4)),
                         ]
    },

}
