#!/usr/bin/python3
from collections import defaultdict
import sys

ar = defaultdict(list)

for line in sys.stdin:
    key, val = line.strip().split("\t", 1)
    ar[key].append(val)

for key, values in ar.items():
    result_array = [0] * 1683

    for val in values:
        a = val.split("\t")
        it = int(a[0])
        result_array[it] = 1
        print(f"{key}\t{val}")

    for i in range(1, 1683):
        if result_array[i] == 0:
            print(f"{key}\t{i}\t0")
