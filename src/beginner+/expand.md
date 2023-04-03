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

Writing this list out is annoying and error prone, because parts of every
filename are identical and repeated.

Even worse, if you need to use this list it in multiple places, it will
be error prone to duplicate it: you are likely to want to add, remove,
or edit elements of the list, and you will need to change it in multiple
places.

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

In the example above, we provide a single pattern, `{acc}.fna.gz.sig`,
and ask `expand` to resolve it into many filenames by filling in values for
the field name `acc` from each element in `ACCESSIONS`. (You may recognize
the keyword syntax for specifying values, `acc=ACCESSIONS`, from
[input and output blocks](input-and-output-blocks.md).)

The result of `expand('{acc}.fna.gz.sig', acc=...)` here is
_identical_ to writing out the four filenames in long form:
```
"GCF_000017325.1.fna.gz.sig",
"GCF_000020225.1.fna.gz.sig",
"GCF_000021665.1.fna.gz.sig",
"GCF_008423265.1.fna.gz.sig"
```
That is, `expand` doesn't do any special wildcard matching or pattern
inference - it just fills in the values and returns the resulting list.

Here, `ACCESSIONS` can be any Python _iterable_ - for example a list, a tuple, 
or a dictionary.  See the [Python appendix](../appendix/python.md) for
details.

## Using `expand` with multiple lists of values

You can also use `expand` with multiple field names. Consider:
```
expand('{acc}.fna.{extension}`, acc=ACCESSIONS, extension=['.gz.sig', .gz'])
```
This will produce the following eight filenames:
```
"GCF_000017325.1.fna.gz.sig",
"GCF_000017325.1.fna.gz",
"GCF_000020225.1.fna.gz.sig",
"GCF_000020225.1.fna.gz",
"GCF_000021665.1.fna.gz.sig",
"GCF_000021665.1.fna.gz",
"GCF_008423265.1.fna.gz.sig",
"GCF_008423265.1.fna.gz"
```
by building every combination of `acc` and `extension`.

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

For more information see the [snakemake documentation on using zip instead of product](https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do).

## Getting a list of identifiers to use in `expand`

The `expand` function provides an effective solution when you have
lists of identifiers that you use multiple times in a workflow - a common
pattern in bioinformatics!  Writing these lists out in a Snakefile
(as we do in the above examples) is not always practical, however;
you may have dozens to hundreds of identifiers!

Lists of identifiers can be loaded from _other_ files in a variety of
ways, and they can also be generated from the set of actual files in
a directory using `glob_wildcards`.

(Provide recipes: loading from file, CSV; config YAML; using glob_wildcards)

## Examples

### Loading a list of accessions from a text file

If you have a simple list of accessions in text file, like so:

```
{{#include ../../code/examples/load_idlist_from/accessions.txt}}
```

then the following code loads each line in the text file in as a separate
ID:
```python
{{#include ../../code/examples/load_idlist_from/snakefile.load_txt}}
```

and builds sourmash signatures for it.

### Loading a specific column from a CSV file

If instead of a text file you have a CSV file with multiple columns,
and the IDs to load are all in one column, you can use the Python
pandas library to read in the CSV. In the code below,
`pandas.read_csv` loads the CSV into a pandas DataFrame object, and then
we select the `accession` column and use that as a list.

@CTB link to pandas.

```csv
{{#include ../../code/examples/load_idlist_from/accessions.csv}}
```

```python
{{#include ../../code/examples/load_idlist_from/snakefile.load_csv}}
```

### Using `glob_wildcards`

```python
{{#include ../../code/examples/load_idlist_from/snakefile.glob_wildcards}}
```

### Loading from the config file

Snakemake also supports the use of configuration files, where the snakefile
supplies the name of the a default config file, which can be overridden
on the command line.

A config file can also be a good place to put accessions. Consider:

```yaml
{{#include ../../code/examples/load_idlist_from/config.yml}}
```

which is used by the following Snakefile:
```python
{{#include ../../code/examples/load_idlist_from/snakefile.use_config}}
```

### Example combining `glob_wildcards`.

link to example in wildcards, renaming recipe in recipes?

A common pattern: get list of files and 

CTB note: link to Python list docs.
CTB note: cover multiext too?
CTB note: cover options to expand? see snakemake.io code

## Links and references

* [Snakemake reference documentation for expand](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#the-expand-function)
* The [Python `itertools`](https://docs.python.org/3/library/itertools.html) documentation.
