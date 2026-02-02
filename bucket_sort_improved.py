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
    bucket_size = 100_000
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

    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", "better_sorting")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(sorted_array)  

better_sorting_log()