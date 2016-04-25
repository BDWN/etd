# config.py
# bladiebla

main = {

    "bench_path": "bench",
    "out_path": "output"

}

gem5 = {

    "path": "/home/bdwn/uni/y3/thesis/gem5/",
    "exec": "/home/bdwn/uni/y3/thesis/gem5/build/ARM/gem5.opt",
    "out_dir": "m5out",
    "script": "se.py",
    "sim_flags": "--cpu-type=TimingSimpleCPU \
                  --caches \
                  --l1d_size=64kB \
                  --l1i_size=16kB \
                  --l2cache \
                  --l2_size=128kB \
                  "

}
