#! /usr/bin/env python
import sys

data = open(sys.argv[1], 'rt').readlines()

for i in data:
    if 'ANCHOR' not in i:
        sys.stdout.write(i)
