#! /usr/bin/env python
import sys
from difflib import unified_diff

data1 = open(sys.argv[1], 'rt').readlines()
data2 = open(sys.argv[2], 'rt').readlines()

#x = "".join():

x = list(unified_diff(data1, data2))
for i in x[3:]:
    sys.stdout.write(i)
