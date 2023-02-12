# Using wildcards to generalize your rules

As we showed in [Chapter 6](../chapter_6.md), when you have repeated
substrings between input and output, you can extract them into
wildcards - going from

```python
rule sketch_genomes_1:
    input:
        "genomes/GCF_000017325.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} --name-from-first
    """
```

to

```python
rule sketch_genomes_1:
    input:
        "genomes/{accession}.fna.gz",
    output:
        "{accession}.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
```

Here, `{accession}` is a wildcard that "fills in" as needed for any filename
that is in the `genomes/` directory and ends with `.fna.gz`.

In this simple (and very common!) use case for wildcards,
snakemake uses pattern matching to see whether, when
missing a desired output (here a filename ending in `.fna.gz.sig`),
there is a corresponding input file; and if so, it runs the associated
shell command, filling in the filename wherever `{accession}` is provided.

This is incredibly useful and means that in many cases you can write
a single rule that is applied to hundreds or thousands of files!

However, there are a lot of subleties to consider. In this
chapter, we're going to cover the most important of those subtleties, and
provide links where you can learn more.

## Rules for wildcards

### Wildcards are local to each rule

Wildcard names only match _within_ a rule block. You can use the same
wildcard names in multiple rules for consistency, but snakemake won't
treat them any differently based on their shared name.

So, for example, this:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{b}.second.txt"
    output: "{b}.third.txt"
```

is equivalent to:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{b}.second.txt"
    output: "{b}.third.txt"
```

One exception is when you use
[global wildcard constraints](../reference/wildcard-constraints.md) to
constrain wildcard matching by wildcard name: there, the constraints
apply across all uses of that wildcard name in the Snakefile.

<!-- CTB: fix link to point directly to global wildcard constraints. -->

A good convention is to choose wildcards to have the same semantic
meaning across the Snakefile - e.g. always use `sample` to mean the
same thing. This makes reading the Snakefile easier!

As a corollary, you can mix and match wildcards. @CTB. Draft text: Since
snakemake is _just_ pattern matching to strings, you can have some rules that
use wildcards to include patterns that are broken down into separate wildcards
by other rules. See examples below.

### Wildcards are automatically available in `input:` and `output:` blocks, but not in other blocks.
    
Within the `input:` and `output:` blocks in a rule, you can refer to
wildcards directly by name. If you want to use wildcards in other
parts of a rule you need to use the `wildcards.` prefix.

Consider this Snakefile:

```python
# this does not work:

rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {a}
```

Here you will get "unknown variable a" @@CTB.

To refer to `{a}` here, you need to use `wildcards.a` in
the shell block:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {wildcards.a}
```

Note that the `wildcards` namespace is only available _within_ a rule -
that's because wildcards only exist within individual rules, and wildcards
are not shared across rules!

### All wildcards used in a rule must match to wildcards in the `output:` block

snakemake uses the wildcards in the `output:` block to fill in the wildcards
elsewhere in the rule, so they have to match across the blocks.

So, for example, every wildcard in the `input:` block needs to be used
in `output:`.  Consider:

```python
# this does not work:

rule analyze_sample:
    input: "{sample}.x.{analysis}.in"
    output: "{sample}.out"
```
because snakemake doesn't know how to fill in the `analysis` wildcard in
the _input_ block.

Think about it this way: if this worked, there would be multiple
different input files for the same output, and snakemake would
have no way to choose which input file to use.

There are situations where wildcards in the `output:` block do _not_ need
to be in the `input:` block, however - see section CTBXXX below on
using wildcards to determine parameters for the shell block.

### Wildcards match greedily, unless constrained

Wildcard pattern matching chooses the _longest possible_ match to
_any_ characters, which can sometimes cause problems. (CTB: example?
Probably prefix/suffix...)

CTB fixme, from snakemake docs:
>Multiple wildcards in one filename can cause ambiguity. 

You can use
[wildcard constraints](../reference/wildcard-constraints.md) to limit
wildcard matching.  In particular, I sometimes find it useful to avoid
having wildcards match to files in subdirectories:

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:no-subdir}}
```

See the [wildcard constraints](../reference/wildcard-constraints.md)
section for more details!

## Some examples of wildcards

### Running one rule on many files

handcoding list of files

### Renaming files using a single wildcard

glob_wildcards

### Renaming files using multiple wildcards

https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do


```
F3D141_S207_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq
```

```python
{{#include ../../code/examples/wildcards.renaming/Snakefile}}
```

note: includes files in subdirectories!

### mixing/matching strings

### constraining wildcards to avoid (e.g.) subdirectories, periods

### Using wildcards to determine parameters to use in the shell block.

You can also use wildcards to build rules that produce output files
where the contents are based on the filename; for example, consider
this example of how to generate a subset of a FASTQ file:

```python
{{#include ../../code/examples/wildcards.subset/Snakefile}}
```

Here, the wildcard is _only_ in the output filename, not in the
input filename. The wildcard value is used by snakemake to determine
how to fill in the number of lines for `head` to select from the file!

This can be really useful for generating files with many different
parameters to a particular shell command - "parameter sweeps". See CTB XXX.

CTB link to:
* params functions, params lambda?
* parameter sweeps with this and expand

## CTB: More things to discuss

Mention:

* here, snakemake is constructing strings to run, that is all.
* simple renaming foo
* pair vs metagenome/genome - jean setup.

## Additional references

See also:
* the [snakemake docs on wildcards](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-wildcards)
