import numpy as np
import time
import matplotlib.pyplot as plt
from bucket_sort_improved import better_sorting_benchmarks
# ---------------- CONFIG ----------------
N = 20_000
REPEATS = 3
MAX_VALUES = [10**i for i in range(1, 7)]  # 10 → 10.000.000

np.random.seed(42)

# ---------------------------------------
# Normal Counting sort implementation
# ---------------------------------------

def counting_sort(arr):
    max_value = 0
    for i in range(len(arr)):
        if max_value < arr[i]:
            max_value = arr[i]

    temp_array = [0] * (max_value + 1)

    for v in arr:
        temp_array[v] += 1

    out = []
    for i, c in enumerate(temp_array):
        out.extend([i] * c)

    return out

# ---------------------------------------
# Better Counting sort implementation
# ---------------------------------------

# ---------------------------------------
# Benchmark
# ---------------------------------------

counting_avg = []
better_counting_avg = []

for max_val in MAX_VALUES:
    base = np.random.randint(0, max_val, size=N)

    ct, qt = [], []

    for _ in range(REPEATS):
        a1 = base.copy()
        a2 = base.copy()

        t0 = time.perf_counter()
        counting_sort(a1)
        ct.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        better_sorting_benchmarks(a2)
        qt.append(time.perf_counter() - t0)

    counting_avg.append(sum(ct) / REPEATS)
    better_counting_avg.append(sum(qt) / REPEATS)


# ---------------------------------------
# Plot
# ---------------------------------------
plt.figure(figsize=(9, 6))

# Medido
plt.plot(MAX_VALUES, counting_avg, "o-", label="Normal Counting sort (medido)")
plt.plot(MAX_VALUES, better_counting_avg, "o-", label="Better Counting sort (medido)")


plt.xscale("log")
plt.yscale("log")
plt.xlabel("MAX_VALUE (k)")
plt.ylabel("Tiempo (s)")
plt.title("Teoría vs práctica: Counting sort vs Better Counting sorttt")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.show()

# ---------------------------------------
# Time Statistics
# ---------------------------------------

print("*** TIME USAGE ***\n")
print("Counting sort:\n")
for i in counting_avg:
    print(round(i, 5))

print("Better Counting sort:\n")
for i in better_counting_avg:
    print(round(i, 5))
    
print("*** SPEEDUP: COUNTING vs Better Counting ***\n")
for i in range(len(counting_avg)):
    speedup = better_counting_avg[i] / counting_avg[i]
    print(f"Counting es {speedup:.2f}× más rápido")