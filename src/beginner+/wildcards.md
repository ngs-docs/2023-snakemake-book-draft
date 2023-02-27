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

Snakemake uses simple _pattern matching_ to determine the value of
`{accession}` - if asked for a filename ending in `.fna.gz.sig`, snakemake
takes the prefix, and then looks for the matching input file
`genomes/{accession}.fna.gz`, and fills in `{input}` accordingly.

This is incredibly useful and means that in many cases you can write
a single rule that is applied to hundreds or thousands of files!

However, there are a lot of subleties to consider. In this
chapter, we're going to cover the most important of those subtleties, and
provide links where you can learn more.

## Rules for wildcards

### Wildcards are determined by the desired output

The first and most important rule of wildcards is this: snakemake
fills in wildcard values based on the filename it is asked to produce.

Consider the following rule:

```python
{{#include ../../code/examples/wildcards.output/snakefile.output}}
```
The wildcard in the output block will match _any_ file that ends with
`.a.out`, and the associated shell command will create it!  This is both
powerful and constraining: you can create any file with the suffix
`.a.out` - but you also need to _ask_ for the file to be created.

This means that somewhere, in either the snakefile on or on the command line,
you need to request a file that ends in `.a.out` in order for snakemake to
fill in the wildcard. There's no other way for snakemake to guess at the
value of the wildcard.

Among other implications, this means that once you put a wildcard in a
rule, you can no longer run that rule by the rule name - you have to
ask for a filename, instead.  If you try to run a rule that contains a
wildcard but don't tell it what filename you want to create, you'll get:
```
Target rules may not contain wildcards.
```

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
    input: "{a}.second.txt"
    output: "{a}.third.txt"
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

An interesting addendum: because wildcards are local to each rule, you
are free to match different parts of patterns in different rules!
See "Mixing and matching wildcards", below. (CTB)

### Wildcards are automatically available in `input:` and `output:` blocks, but not in other blocks.
    
Within the `input:` and `output:` blocks in a rule, you can refer to
wildcards directly by name. If you want to use wildcards in other
parts of a rule you need to use the `wildcards.` prefix. Here,
`wildcards` is a _namespace_, which we will talk about more later. (CTB)

Consider this Snakefile:

```python
# this does not work:

rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {a}"
```

Here you will get an error,
```
NameError: The name 'a' is unknown in this context. Did you mean 'wildcards.a'?
```

As the error suggests, you need to use `wildcards.a` in
the shell block instead:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {wildcards.a}"
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
fastqc or gzip?
all files/all subdirectories

### Renaming files by prefix using `glob_wildcards`

Consider a set of files named like so:

```
F3D141_S207_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq
```
within the `original/` subdirectory.

Now suppose you want to rename them all to get rid of the `_001` suffix
before `.fastq`. This is very easy with wildcards!

The below Snakefile uses `glob_wildcards` to load in a list of files from
a directory and then make a copy of them with the new name under the
`renamed/` subdirectory:

```python
{{#include ../../code/examples/wildcards.renaming_simple/Snakefile}}
```

Here you could do a `mv` instead of a `cp` and then the glob_wildcards would no longer pick
up the changed files after running.

### Renaming files using multiple wildcards



```python
{{#include ../../code/examples/wildcards.renaming/Snakefile}}
```

note: includes files in subdirectories!

Links:

* [snakemake documentation on using zip instead of product](https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do)

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
