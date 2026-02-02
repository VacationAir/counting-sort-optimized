import numpy as np
import time
import matplotlib.pyplot as plt
import math
from multiprocessing import Pool, cpu_count, freeze_support, set_start_method
import psutil
import os
from tqdm import tqdm
from multiprocessing import Manager

# ---------------- CONFIG ----------------
N = 10
REPEATS = 4
MAX_VALUES = [10**i for i in range(8, 14)]

np.random.seed(42)

# ---------------------------------------
# COUNTING SORT ORIGINAL
# ---------------------------------------
def counting_sort_original(arr):
    max_value = 0
    for v in arr:
        if v > max_value:
            max_value = v

    temp_array = [0] * (max_value + 1)

    for v in arr:
        temp_array[v] += 1

    out = []
    for i, c in enumerate(temp_array):
        out.extend([i] * c)

    return out


# ---------------------------------------
# BETTER SORT
# ---------------------------------------
def better_sorting_benchmarks(array):

    MAX_VALUE = max(array)

    bucket_size = 5
    num_buckets = (MAX_VALUE // bucket_size) + 1
    buckets = [[] for _ in range(num_buckets)]

    for value in array:
        buckets[value // bucket_size].append(value)

    for bucket in buckets:
        if not bucket:
            continue

        local_min = bucket[0]
        local_max = bucket[0]

        for v in bucket[1:]:
            if v > local_max:
                local_max = v
            elif v < local_min:
                local_min = v

        size = local_max - local_min + 1
        count = [0] * size

        for v in bucket:
            count[v - local_min] += 1

        idx = 0
        for i in range(size):
            val = i + local_min
            for _ in range(count[i]):
                bucket[idx] = val
                idx += 1

    result = []
    for bucket in buckets:
        result.extend(bucket)

    return result


# ---------------------------------------
# QUICK SORT
# ---------------------------------------
def quicksort_py(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left, middle, right = [], [], []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)

    return quicksort_py(left) + middle + quicksort_py(right)


# ---------------------------------------
# WORKER PARALLELO
# ---------------------------------------
def run_benchmark(args):

    base, max_val, stats = args

    proc = psutil.Process(os.getpid())
    ram_mb = proc.memory_info().rss / 1024**2
    ct_orig, ct_better, qt = [], [], []

    for r in range(REPEATS):

        mem0 = proc.memory_info().rss

        # ORIGINAL
        a1 = base.copy().tolist()
        stats["lists"] += 1
        t0 = time.perf_counter()
        counting_sort_original(a1)
        ct_orig.append(time.perf_counter() - t0)

        # BETTER
        a2 = base.copy().tolist()
        stats["lists"] += 1
        t0 = time.perf_counter()
        better_sorting_benchmarks(a2)
        ct_better.append(time.perf_counter() - t0)

        # QUICK
        a3 = base.copy().tolist()
        stats["lists"] += 1
        t0 = time.perf_counter()
        quicksort_py(a3)
        qt.append(time.perf_counter() - t0)

        mem1 = proc.memory_info().rss

        stats["tasks_done"] += 1

        print(
            f"[PID {os.getpid()}] "
            f"repeat={r}  "
            f"RAM={(mem1-mem0)/1e6:.1f}MB  "
            f"lists={stats['lists']}"
            f" RAM = {ram_mb}"
        )

    return (
        sum(ct_orig)/REPEATS,
        sum(ct_better)/REPEATS,
        sum(qt)/REPEATS
    )


# ---------------------------------------
# MAIN (🔥 OBLIGATORIO EN WINDOWS 🔥)
# ---------------------------------------
def main():
    from multiprocessing import Manager

    manager = Manager()
    stats = manager.dict()
    stats["lists"] = 0
    stats["tasks_done"] = 0

    tasks = []

    for max_val in MAX_VALUES:
        base = np.random.randint(0, max_val, size=N, dtype=np.int64)
        tasks.append((base, max_val, stats))

    print(f"\n🔥 Using {cpu_count()} cores\n")

    results = []

    with Pool(processes=cpu_count()) as p:

        for r in tqdm(
            p.imap_unordered(run_benchmark, tasks),
            total=len(tasks),
            desc="Benchmarking"
        ):
            results.append(r)

    # ---------------- unpack results
    counting_original_avg = [r[0] for r in results]
    counting_better_avg = [r[1] for r in results]
    quick_avg = [r[2] for r in results]

    # ---------------- THEORETICAL
    theoretical_counting = [N + k for k in MAX_VALUES]
    theoretical_quick = [N * math.log2(N)] * len(MAX_VALUES)

    scale_count = counting_original_avg[0] / theoretical_counting[0]
    scale_quick = quick_avg[0] / theoretical_quick[0]

    theoretical_counting = [x * scale_count for x in theoretical_counting]
    theoretical_quick = [x * scale_quick for x in theoretical_quick]

    # ---------------- PLOT
    plt.figure(figsize=(10, 7))

    plt.plot(MAX_VALUES, counting_original_avg, "o-", label="Counting original", linewidth=2)
    plt.plot(MAX_VALUES, counting_better_avg, "s-", label="Better counting", linewidth=2)
    plt.plot(MAX_VALUES, quick_avg, "o-", label="Quicksort", linewidth=2)

    plt.plot(MAX_VALUES, theoretical_counting, "--", label="n+k", alpha=0.5)
    plt.plot(MAX_VALUES, theoretical_quick, "--", label="n log n", alpha=0.5)

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("MAX_VALUE")
    plt.ylabel("Time (s)")
    plt.title(f"CPU benchmark on i5-12600KF — N={N:,}")

    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()



# ---------------------------------------
if __name__ == "__main__":

    from multiprocessing import freeze_support, set_start_method

    freeze_support()

    try:
        set_start_method("spawn")
    except RuntimeError:
        pass

    main()
