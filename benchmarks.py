# benchmarks.py
# bladiebla

from input import Types

benchmarks = {
                "fac"        : [ ("i_1", (Types.int, 0, 3))],
                "recursion"  : [ ("i_1", (Types.int, 0, 100))],
                "prime"      : [ ("i_1", (Types.int, 0, 100000))],
                "bsort"      : [ ("a_1", (Types.uniquearray, 4))],
                "insertsort" : [ ("a_1", (Types.array, 5))]
             }
