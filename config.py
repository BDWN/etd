# config.py

main = {

    # Directory to which all output is saved
    "out_dir": "output"

}

gem5 = {

    # Gem5 simulator main path
    "path": "/home/bdwn/uni/y3/thesis/gem5/",

    # Gem5 simulator binary
    "exec": "/home/bdwn/uni/y3/thesis/gem5/build/ARM/gem5.opt",

    # Script with which to run Gem5
    "script": "se.py",

    # Arguments passed to simulator script
    "script_args": "--cpu-type=TimingSimpleCPU \
                    --caches \
                    --l1d_size=64kB \
                    --l1i_size=16kB \
                    --l2cache \
                    --l2_size=128kB \
                    ",
    # "script_args": "--cpu-type=TimingSimpleCPU ",

    # Output directory name for simulator statistics:
    # 'out_dir'/'benchmark_name'/'out_dir'/
    "out_dir": "m5out",

}

benchmark = {

    # Resulting output file created by running benchmark
    "out_file": "cycles",
    "out_ext": "csv",

    # Filename of benchmark executable, must correspond with filename specified
    # in benchmark Makefile
    "bench_exec": "a.out",

}
