#! /usr/bin/env python
"""
Find all files matching 'Snakefile' or 'snakefile.*', and write shell
code to run them. Very much a WIP.

TODO?
- set bash foo
- write individual shell scripts => support parallel??
- support isolated build/etc directories
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path


PATH_FILTERS = []

remove_out = lambda p: str(p).endswith('.out')
PATH_FILTERS.append(remove_out)

remove_bak = lambda p: str(p).endswith('~') or str(p).endswith('.bak')
PATH_FILTERS.append(remove_bak)

remove_dot = lambda p: any(pp.startswith('.') for pp in p.parts)
PATH_FILTERS.append(remove_dot)


def read_snakefile_metadata(filename):
    d = {}
    with open(filename, 'rt') as fp:
        lines = []
        for line in fp:
            line = line.strip()
            if not line.startswith('#'):
                break

            line = line[1:].strip()
            lines.append(line)

    d['expect_fail'] = False
    if 'expect_fail' in lines:
        d['expect_fail'] = True

    d['ignore'] = False
    if 'ignore' in lines:
        d['ignore'] = True

    for x in lines:
        if x.startswith('targets:'):
            x = x[8:]
            d['targets'] = x.strip()

    return d


def main():
    p = argparse.ArgumentParser()
    p.add_argument('dirs', nargs='+')
    p.add_argument('-o', '--output', default=None)
    p.add_argument('-l', '--list-snakefiles', action='store_true')
    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('-q', '--quiet', action='store_true')
    p.add_argument('-k', '--keyword-limit-pattern', default=None,
                   help="specify keyword required in filename to run")
    args = p.parse_args()

    snakefiles = []
    for dirname in args.dirs:
        pp = Path(dirname)

        snakefiles.extend(pp.glob('**/Snakefile'))
        snakefiles.extend(pp.glob('**/snakefile.*'))

    # filter:
    snakefiles_filtered = []
    for ss in snakefiles:
        if any(f(ss) for f in PATH_FILTERS):
            if args.debug:
                print(f"(removing '{str(ss)}' from paths because of a filter)",
                      file=sys.stderr)
            continue

        if args.keyword_limit_pattern:
            if args.keyword_limit_pattern not in str(ss):
                continue

        # keep!
        snakefiles_filtered.append(ss)

    snakefiles = snakefiles_filtered
        
    print(f"found {len(snakefiles)} snakefiles to run!", file=sys.stderr)

    if args.list_snakefiles:
        print("\n".join([ str(ss) for ss in snakefiles ]))

    if args.output:
        print(f"Saving run script to '{args.output}'", file=sys.stderr)
        output = open(args.output, 'wt')

        for snakefile in snakefiles:
            targets = ''
            metadata = read_snakefile_metadata(snakefile)

            if 'ignore' in metadata and metadata['ignore']:
                if not args.quiet:
                    print(f"(IGNORING '{snakefile}' per metadata)",
                          file=sys.stderr)
                continue
            
            if 'targets' in metadata:
                targets = metadata['targets']
            dirname, filename = os.path.split(snakefile)

            if metadata['expect_fail']:
                print(f"""
cd {dirname}
snakemake -s {filename} -j 1 -p {targets} >& {filename}.out && echo fail {snakefile} || echo success
cd - > /dev/null
""", file=output)
            else:
                print(f"""
cd {dirname}
snakemake -s {filename} -j 1 -p {targets} >& {filename}.out && echo success || echo fail {snakefile}
cd - > /dev/null
""", file=output)

        print("exit 0", file=output)


if __name__ == '__main__':
    sys.exit(main())
