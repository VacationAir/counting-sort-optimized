import numpy as np
import time
import matplotlib.pyplot as plt
from bucket_sort_improved import better_sorting_benchmarks, better_magnitude_sorting_benchmarks, better_sorting_by_units_benchmarks

# ---------------- CONFIG ----------------
N = 10_000
REPEATS = 3
MAX_VALUES = [10**i for i in range(1, 9)]  # 10 → 10.000.000
np.random.seed(42)

# ---------------------------------------
# COUNTING SORT ORIGINAL 
# ---------------------------------------
def counting_sort_original(arr):
    max_value = max(arr)
    temp_array = [0] * (max_value + 1)
    for v in arr:
        temp_array[v] += 1
    out = []
    for i, c in enumerate(temp_array):
        out.extend([i] * c)
    return out

# ---------------------------------------
# Quick sort implementation
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
# Benchmark
# ---------------------------------------
results = {
    "Counting original": [],
    "Better counting": [],
    "Magnitude bucket": [],
    "Digit magnitude bucket": [],
    "Quicksort Py": [],
    "Python sort": []
}



for max_val in MAX_VALUES:
    base = np.random.randint(0, max_val, size=N)

    ct_orig, ct_better, mbt,qt, py_sort, ddbt = [], [], [], [], [], []

    for _ in range(REPEATS):
        # 1. Counting sort original
        a1 = base.copy().tolist()
        t0 = time.perf_counter()
        counting_sort_original(a1)
        ct_orig.append(time.perf_counter() - t0)

        # 2. Better Counting sort lista
        a2 = base.copy().tolist()
        t0 = time.perf_counter()
        better_sorting_benchmarks(a2)
        ct_better.append(time.perf_counter() - t0)

        # 3. Magnitude counting bucket sort
        a3 = base.copy().tolist()
        t0 = time.perf_counter()
        better_magnitude_sorting_benchmarks(a3)
        results_tmp = time.perf_counter() - t0
        mbt.append(results_tmp)

        # 4. Quicksort Python
        a4 = base.copy().tolist()
        t0 = time.perf_counter()
        quicksort_py(a4)
        qt.append(time.perf_counter() - t0)

        # 5. Python sort nativo
        a5 = base.copy().tolist()
        t0 = time.perf_counter()
        sorted(a5)
        py_sort.append(time.perf_counter() - t0)
        # 6. Magnitude by digits counting
        a6 = base.copy().tolist()
        t0 = time.perf_counter()
        better_sorting_by_units_benchmarks(a4)
        ddbt.append(time.perf_counter() - t0)

    # Promedio de tiempos
    results["Counting original"].append(sum(ct_orig)/REPEATS)
    results["Better counting"].append(sum(ct_better)/REPEATS)
    results["Magnitude bucket"].append(sum(mbt)/REPEATS)
    results["Quicksort Py"].append(sum(qt)/REPEATS)
    results["Python sort"].append(sum(py_sort)/REPEATS)
    results["Digit magnitude bucket"].append(sum(ddbt)/REPEATS)

# ---------------------------------------
# Plot
# ---------------------------------------
plt.figure(figsize=(12, 8))
for key, times in results.items():
    plt.plot(MAX_VALUES, times, marker="o", label=key, linewidth=2)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("MAX_VALUE (k)")
plt.ylabel("Tiempo (s)")
plt.title(f"Comparación de algoritmos de ordenamiento (N={N:,})")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------------------
# Tabla de resultados
# ---------------------------------------
print("\nRESUMEN DE TIEMPOS (segundos)")
print("="*80)
print(f"{'MAX_VALUE':>12} {'Counting':>12} {'Better':>12} {'Magnitude':>12} {'Quicksort':>12} {'Python sort':>12}{'Digit Magnitude':>12}")
print("-"*80)
for i in range(len(MAX_VALUES)):
    print(
    f"{MAX_VALUES[i]:>12} "
    f"{results['Counting original'][i]:>12.5f} "
    f"{results['Better counting'][i]:>12.5f} "
    f"{results['Magnitude bucket'][i]:>12.5f} "
    f"{results['Quicksort Py'][i]:>12.5f} "
    f"{results['Python sort'][i]:>12.5f}"
    f"{results["Digit magnitude bucket"][i]:>12.5f}"
)
print("="*80)
