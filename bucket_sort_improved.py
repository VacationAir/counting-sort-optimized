import numpy as np
import time
import math
import csv
import os

def normal_sorting():
    # Generate Array with numbers
    array = np.zeros(2000)

    for i in range(len(array)):
        array[i] = np.random.randint(0,10**14, dtype=np.int64)

    # Find maximum
    start = time.perf_counter()
    max = 0
    for i in range(len(array)):
        if max < array[i]:
            max = array[i]
    
    # Sorting
    temp_array = [0] * max

    for value in array.astype(int):
        temp_array[value] += 1

    sorted_array = [] 

    for index, quantity in enumerate(temp_array):
        sorted_array.extend([index] * quantity)

    end = time.perf_counter()
    print(array)
    print(sorted_array)
    print("Counting sort time:", end - start)

def better_sorting():
    # Generate Array with numbers
    array = np.zeros(200000)

    for i in range(len(array)):
        array[i] = np.random.randint(0,10**10, dtype=np.int64)

    # Find maximum
    MAX_VALUE = 0
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
    
    # Sorting
    bucket_size = 5
    num_buckets = int((MAX_VALUE // bucket_size) + 1)
    buckets = [np.zeros(bucket_size, dtype=np.int64) for _ in range(num_buckets)]

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
    sorted_array = np.concatenate(buckets)


    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", "better_sorting")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(sorted_array)  
    
def better_sorting_log():
    timings = {}

    # ---------------- GENERATE ARRAY ----------------
    start = time.perf_counter()
    array = np.zeros(2_000_000, dtype=np.int64)
    for i in range(len(array)):
        array[i] = np.random.randint(0, 10**10, dtype=np.int64)
    timings["generate_array"] = time.perf_counter() - start

    # ---------------- FIND MAX ----------------
    start = time.perf_counter()
    MAX_VALUE = 0
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
    timings["find_max"] = time.perf_counter() - start

    # ---------------- DISTRIBUTE INTO BUCKETS ----------------
    start = time.perf_counter()
    bucket_size = 5
    num_buckets = int((MAX_VALUE // bucket_size) + 1)
    buckets = [[] for _ in range(num_buckets)]
    for value in array:
        bucket_index = int(value // bucket_size)
        buckets[bucket_index].append(value)
    timings["distribute_buckets"] = time.perf_counter() - start

    # ---------------- COUNTING SORT PER BUCKET ----------------
    start = time.perf_counter()
    for arr in buckets:
        if len(arr) != 0:
            local_max = arr[0]
            local_min = arr[0]
            # Find local min/max
            for number in arr:
                if local_max < number:
                    local_max = number
                if local_min > number:
                    local_min = number
            # Counting sort
            temp = [0] * (int(local_max - local_min) + 1)
            for number in arr:
                temp[int(number - local_min)] += 1

            sorted_array = []
            for index, quantity in enumerate(temp):
                sorted_array.extend([index + local_min] * quantity)
            arr[:] = sorted_array
    timings["counting_sort_buckets"] = time.perf_counter() - start

    # ---------------- MERGE BUCKETS ----------------
    start = time.perf_counter()
    sorted_array = []
    for arr in buckets:
        if len(arr) != 0:
            sorted_array.extend(arr)
    timings["merge_buckets"] = time.perf_counter() - start

    # ---------------- SAVE RESULTS ----------------
    start = time.perf_counter()
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", "better_sorting.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(sorted_array)
    timings["save_results"] = time.perf_counter() - start

    # ---------------- LOG TIMINGS ----------------
    for key, value in timings.items():
        print(f"{key:25}: {value:.4f} s")

def better_sorting_benchmarks(array):
    # Find maximum
    MAX_VALUE = 0
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
    
    # Sorting
    bucket_size = max(100_000, MAX_VALUE // len(array))  

    num_buckets = 100_000
    buckets = [[] for _ in range(num_buckets)]

    bucket_min = [float("inf")] * num_buckets
    bucket_max = [float("-inf")] * num_buckets
    for value in array:
        bucket_index = int(value // bucket_size)
        buckets[bucket_index].append(value)
        if value < bucket_min[bucket_index]:
            bucket_min[bucket_index] = value
        if value > bucket_max[bucket_index]:
            bucket_max[bucket_index] = value

    # Counting sort
    for i, array in enumerate(buckets):
        if len(array) != 0:

            temp = [0] * (int(bucket_max[i] - bucket_min[i]) +1)
            for number in array:
                temp[int(number - bucket_min[i])] += 1
                
            total_elements = sum(temp)  
            sorted_array = [0] * total_elements  
            pos = 0
            for index, quantity in enumerate(temp):
                for _ in range(quantity):
                    sorted_array[pos] = index + bucket_min[i]
                    pos += 1

def better_magnitude_sorting_benchmarks(arr):
    array = arr.tolist() if hasattr(arr, "tolist") else list(arr)

    n = len(array)
    if n <= 1:
        return array.copy()

    lo = min(array)
    hi = max(array)
    R = hi - lo + 1

    # Choose bucket size
    approx_buckets = int(math.sqrt(n))
    bucket_size = max(1, R // approx_buckets)

    num_buckets = (R + bucket_size - 1) // bucket_size
    buckets = [[] for _ in range(num_buckets)]

    # Distribution
    for v in array:
        idx = (v - lo) // bucket_size
        buckets[idx].append(v)

    # Local counting
    out = []

    for bucket in buckets:
        if not bucket:
            continue

        bmin = min(bucket)
        bmax = max(bucket)

        counts = [0] * (bmax - bmin + 1)
        for v in bucket:
            counts[v - bmin] += 1

        for i, c in enumerate(counts):
            if c:
                out.extend([i + bmin] * c)

    return out

def better_sorting_by_units_benchmarks(array):
    # Find maximum
    MAX_VALUE = 0
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
    
    # Sorting
    num_buckets = len(str(MAX_VALUE))
    buckets = [[] for _ in range(num_buckets)]

    bucket_min = [float("inf")] * num_buckets
    bucket_max = [float("-inf")] * num_buckets
    for value in array:
        bucket_index = int(math.log10(value)) if value > 0 else 0
        buckets[bucket_index].append(value)
        if value < bucket_min[bucket_index]:
            bucket_min[bucket_index] = value
        if value > bucket_max[bucket_index]:
            bucket_max[bucket_index] = value

    # Counting sort
    for i, array in enumerate(buckets):
        if len(array) != 0:

            temp = [0] * (int(bucket_max[i] - bucket_min[i]) +1)
            for number in array:
                temp[int(number - bucket_min[i])] += 1
                
            total_elements = sum(temp)  
            sorted_array = [0] * total_elements  
            pos = 0
            for index, quantity in enumerate(temp):
                for _ in range(quantity):
                    sorted_array[pos] = index + bucket_min[i]
                    pos += 1
    return sorted_array