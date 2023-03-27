#! /usr/bin/env python
import sys
import os
import argparse
import subprocess


def main():
    p = argparse.ArgumentParser()
    p.add_argument('dirs', nargs='+')
    p.add_argument('-o', '--output', default=None)
    args = p.parse_args()

    x = []
    for dirname in args.dirs:
        for root, dirs, files in os.walk(dirname):
            for name in sorted(files):
                fullname = os.path.join(root, name)
                if fullname.startswith('.') or '/.' in fullname or \
                   fullname.endswith('~'):
                    # skip
                    continue

                if name == 'Snakefile' or name.startswith('snakefile'):
                    assert os.path.exists(fullname)
                    x.append(fullname)

    print(f"found {len(x)} snakefiles to run!", file=sys.stderr)

    output = sys.stdout
    if args.output:
        output = open(args.output, 'wt')

    for snakefile in x:
        dirname, filename = os.path.split(snakefile)
        print(f"""
cd {dirname}
snakemake -s {filename} -j 1 -p -n && echo success || echo fail
cd -
""", file=output)

if __name__ == '__main__':
    sys.exit(main())
