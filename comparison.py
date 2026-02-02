import numpy as np
import time
import matplotlib.pyplot as plt
import math

# ---------------- CONFIG ----------------
N = 3_000_000
REPEATS = 3
MAX_VALUES = [10**i for i in range(1, 8)]  # 10 → 10.000.000

np.random.seed(42)

# ---------------------------------------
# COUNTING SORT ORIGINAL 
# ---------------------------------------
def counting_sort_original(arr):
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
# BETTER SORTING 
# ---------------------------------------
def better_sorting_benchmarks(array):
   # Find maximum
    MAX_VALUE = 0
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
    
    # Sorting
    bucket_size = 5
    num_buckets = int((MAX_VALUE // bucket_size) + 1)
    buckets = [[] for _ in range(num_buckets)]

    for value in array:
        bucket_index = int(value // bucket_size)
        buckets[bucket_index].append(value)

    for array in buckets:
        if len(array) != 0:
            local_max = 0
            local_min = array[0]
            # Counting sort
            for number in array:
                # Find max
                if local_max < number:
                    local_max = number
                if local_min > number:
                    local_min = number

            temp = [0] * (int(local_max - local_min) +1)
            for number in array:
                temp[int(number - local_min)] += 1

            sorted_array = []
            for index, quantity in enumerate(temp):
                sorted_array.extend([index + local_min] * quantity)

            array[:] = sorted_array
    # Merge buckets
    sorted_array = []
    for array in buckets:
        if len(array) != 0:
            for number in range(len(array)):
                sorted_array.append(array[number])
    
    return sorted_array

# ---------------------------------------
# Quick sort implementation
# ---------------------------------------
def quicksort_py(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = []
    middle = []
    right = []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)

    return quicksort_py(left) + middle + quicksort_py(right)

# ---------------------------------------
# Benchmark
# ---------------------------------------

counting_original_avg = []
counting_better_avg = []
quick_avg = []

for max_val in MAX_VALUES:
    base = np.random.randint(0, max_val, size=N)

    ct_orig, ct_better, qt = [], [], []

    for _ in range(REPEATS):
        # Counting sort original
        a1 = base.copy().tolist()
        t0 = time.perf_counter()
        counting_sort_original(a1)
        ct_orig.append(time.perf_counter() - t0)
        
        # Better sorting (tu versión)
        a2 = base.copy().tolist()
        t0 = time.perf_counter()
        better_sorting_benchmarks(a2)
        ct_better.append(time.perf_counter() - t0)
        
        # Quick sort
        a3 = base.copy().tolist()
        t0 = time.perf_counter()
        quicksort_py(a3)
        qt.append(time.perf_counter() - t0)

    counting_original_avg.append(sum(ct_orig) / REPEATS)
    counting_better_avg.append(sum(ct_better) / REPEATS)
    quick_avg.append(sum(qt) / REPEATS)

# ---------------------------------------
# Curvas teóricas
# ---------------------------------------
theoretical_counting = [N + k for k in MAX_VALUES]
theoretical_quick = [N * math.log2(N)] * len(MAX_VALUES)

# Normalización (ajuste visual)
scale_count = counting_original_avg[0] / theoretical_counting[0]
scale_quick = quick_avg[0] / theoretical_quick[0]

theoretical_counting = [x * scale_count for x in theoretical_counting]
theoretical_quick = [x * scale_quick for x in theoretical_quick]

# ---------------------------------------
# Plot
# ---------------------------------------
plt.figure(figsize=(10, 7))

# Medido
plt.plot(MAX_VALUES, counting_original_avg, "o-", label="Counting sort original", linewidth=2)
plt.plot(MAX_VALUES, counting_better_avg, "s-", label="Better Counting sort", linewidth=2)
plt.plot(MAX_VALUES, quick_avg, "o-", label="Quicksort (medido)", linewidth=2)

# Teórico
plt.plot(MAX_VALUES, theoretical_counting, "--", label="n + k (teórico)", alpha=0.5)
plt.plot(MAX_VALUES, theoretical_quick, "--", label="n log n (teórico)", alpha=0.5)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("MAX_VALUE (k)")
plt.ylabel("Tiempo (s)")
plt.title(f"Comparación: Counting sort original vs mejorado (N={N:,})")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

# ---------------------------------------
# Time Statistics
# ---------------------------------------

print("*** TIME USAGE ***\n")
print("Counting sort original:")
for i in counting_original_avg:
    print(f"{i:.5f}")

print("\nBetter Counting sort:")
for i in counting_better_avg:
    print(f"{i:.5f}")

print("\nQuick sort:")
for i in quick_avg:
    print(f"{i:.5f}")

print("\n*** SPEEDUP: BETTER vs ORIGINAL ***\n")
for i in range(len(counting_original_avg)):
    speedup = counting_original_avg[i] / counting_better_avg[i]
    print(f"MAX={MAX_VALUES[i]:>8}: Better es {speedup:.2f}x más rápido que Original")

print("\n*** SPEEDUP: BETTER vs QUICK ***\n")
for i in range(len(counting_better_avg)):
    speedup = quick_avg[i] / counting_better_avg[i]
    if speedup > 1:
        print(f"MAX={MAX_VALUES[i]:>8}: Better es {speedup:.2f}x más rápido que Quick")
    else:
        print(f"MAX={MAX_VALUES[i]:>8}: Quick es {1/speedup:.2f}x más rápido que Better")

# Tabla comparativa
print("\n" + "="*60)
print("RESUMEN DE TIEMPOS (segundos)")
print("="*60)
print(f"{'MAX_VALUE':>12} {'Original':>12} {'Better':>12} {'Quicksort':>12}")
print("-"*60)
for i in range(len(MAX_VALUES)):
    print(f"{MAX_VALUES[i]:>12} {counting_original_avg[i]:>12.5f} {counting_better_avg[i]:>12.5f} {quick_avg[i]:>12.5f}")
print("="*60)

