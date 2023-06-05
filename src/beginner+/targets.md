# Running rules and choosing targets from the command line

The way that you specify targets in snakemake is simple, but can lead
to a lot of complexity in its details.

* key points: what you put on the command line - "targets" - is mirror image
  of snakefile
* snakefile organization can/should reflect
* difference between rule names and filenames; wildcard rules and not.

USe language: "pseudo-rules "

snakemake docs link:
https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#targets-and-aggregation

set:
```
default_target: True
```

## Default targets

If you just run `snakemake -j 1`, snakemake will run the first rule it
encounters. This can be adjusted by @@.

The typical way to use this is to provide a rule 'all' at the top of
the Snakefile that looks like this:
```python
rule all:
    input:
        ...
```
Typically this rule contains one or more input files, and no other
rule blocks; for example, in [Chapter 11](../chapter_11.md), the
default rule 

This is because for rules with no output or shell commands, snakemake
will work to satisfy the rule preconditions (i.e. to generate the
input files), which is all you need for a default rule.

So the default rule, often named `all`, should contain a single input
block which in turns has a list of all of the "default" output output
files that the workflow should produce.

## Concrete targets: using rule names vs using filenames

snakemake will happily take rule names and/or filenames on the command
line, in any mixture. It does not guarantee a particular order to run
them in, although it will generally run them in the order specified on
the command line.

For example, for the Snakefile from [Chapter 11](../chapter_11.md),
you could run `snakemake -j 1 compare_genomes` to execute just the
`compare_genomes` rule, or you could add `plot_comparison` to execute
both `compare_genomes` and `plot_comparison`, or you could just run
`plot_comparison` which will run `compare_genomes` anyway because `plot_comparison` relies on the output of `compare_genomes`.

## Executing wildcard targets using filenames

Rules containing wildcards cannot be executed by rule name, because 
snakemake does not have enough information to fill in the wildcards.

So you could not run `snakemake -j 1 sketch_genomes` because that rule
has a wildcard in it: in order to run the rule, snakemake needs to
fill in the `accession` wildcard, and just giving it the rule name
isn't sufficient.

However, you can run wildcard targets using filenames! If you run
`snakemake -j 1 GCF_000017325.1.fna.gz.sig` then snakemake will
find the rule that produces an output file of that form
(which in this case is the `sketch_genome` rule), and run it, filling
in the wildcard from the specified output file name.

So snakemake will happily run rules by name, as long as they don't contain
wildcards; or it will find and run the rules necessary to produce any
specified files, as long as it can find rules that produce those files;
or a mixture.

## Organizing your workflow with multiple concrete targets

You can provide multiple concrete target names that build specific sets of
files. This is useful when building or debugging your workflow.

Consider again the Snakefile from [Chapter 11](../chapter_11.md). There
are rules to run `sourmash compare` and rules to produce the output plot,
but there isn't a rule that will produce _just_ the signature files.

We can add such a rule easily: somewhere below rule `all`, we would add:
```
rule build_sketches:
    input:
        expand("{acc}.fna.gz.sig", acc=ACCESSIONS)
```
then executing `snakemake -j 1 build_sketches` would produce four
.sig files, and do nothing else.

The difference between this and the `compare_genomes` rule is that
`compare_genomes` also runs `sourmash compare`.

@CTB: recipe with toplevel

## Advice on structuring your snakefile

* provide a default rule
* provide one or more concrete rules that are well named
* do not expect people (including yourself) to remember your filename layout
  or your rule names without documentation ;).

