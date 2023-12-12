#!/usr/bin/python3
# -*-coding:utf-8 -*

import sys

for line in sys.stdin:
    ar = line.strip().split("\t")
    uid = ar[0]
    val = "\t".join([ar[1], ar[2]])
    print(uid , "\t" , val)
