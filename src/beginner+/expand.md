# Using `expand` to generate filenames

[Snakemake wildcards](./wildcards.md) make it easy to apply rules to
many files, but also create a new challenge: how do you generate all the
filenames you want?

As an example of this challenge, consider the list of genomes needed
for rule `compare_genomes` from [Chapter 8](../chapter_8.md) - 

```python
rule compare_genomes:
    input:
        "GCF_000017325.1.fna.gz.sig",
        "GCF_000020225.1.fna.gz.sig",
        "GCF_000021665.1.fna.gz.sig",
        "GCF_008423265.1.fna.gz.sig",
```

Writing this list out is annoying and error prone.

Even worse, if you need to use this list it in multiple places, it will
be error prone to duplicate it.

In [Chapter 9](../chapter_9.md), we changed this to a list of the
accessions at the top of the Snakefile and then used a function called
`expand` to generate the list:
```python
ACCESSIONS = ["GCF_000017325.1",
              "GCF_000020225.1",
              "GCF_000021665.1",
              "GCF_008423265.1"]

#...

rule compare_genomes:
    input:
        expand("{acc}.fna.gz.sig", acc=ACCESSIONS),

```

This is a common pattern in Snakefiles, and in this chapter we'll explore
it more!

## Using `expand` with a single pattern and one list of values



## Using `expand` with multiple patterns and lists

## Generating _all_ combinations vs _pairwise_ combinations

As we saw above, with multiple patterns, `expand` will generate all
possible combinations: that is,
```python
X = [1, 2, 3]
Y = ['a', 'b', 'c']

rule all:
   input:
      expand('{x}.by.{y}', x=X, y=Y)
```
will generate 9 filenames: `1.by.a`, `1.by.b`, `1.by.c`, `2.by.a`, etc.
And if you added a third pattern to the `expand` string, `expand` would
also add that into the combinations!

So what's going on here?

By default, expand does an all-by-all expansion containing all
possible combinations. (This is sometimes
called a Cartesian product, a cross-product, or an outer join.)

But sometimes you don't want that. So how do we change this behavior?

`expand` takes an optional second argument, the combinator, which
tells `expand` how to combine the lists of values the come after. By
default `expand` uses a Python function called `itertools.product`,
which creates all possible combinations.

You can tell `expand` to create pairwise combinations by using `zip` instead -
something we did in one of the [wildcard examples](wildcards.md).

You do this like so:
```python
X = [1, 2, 3]
Y = ['a', 'b', 'c']

rule all:
   input:
      expand('{x}.by.{y}', zip, x=X, y=Y)
```
which will now generate only three filenames: `1.by.a`, `2.by.b`, and `3.by.c`.

* link to snakemake docs here.

## Getting list of files to use in `expand`

## Examples

### Example combining `glob_wildcards`.

link to example in wildcards, renaming recipe in recipes?

A common pattern: get list of files and 

CTB note: link to Python list docs.
CTB note: cover multiext too?
CTB note: cover options to epxand? see snakemake.io code

## Where do you get the accessions from?

a list
read_csv - from a config
glob_wildcards - don't always recommend

