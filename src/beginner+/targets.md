# Running rules and choosing targets from the command line

The way that you specify targets in snakemake is simple, but can lead
to a lot of complexity in its details.

## Default targets

If you just run `snakemake -j 1`, snakemake will run the first rule it
encounters. This can be adjusted by @@.

The typical way to use this is to provide a rule 'all' at the top of
the Snakefile that looks like this: @@. Often these rules contain only
a list of input files, as in Chapter XYZ; for rules with no output or
shell commands, snakemake will work to satisfy the rule preconditions
(i.e. to generate the input files), which is what you want.

## Concrete targets: using rule names vs using filenames

snakemake will happily take rule names and/or filenames on the command
line, in any mixture. It does not guarantee a particular order to run
them in, although it will generally run them in the order specified on
the command line.

## Executing wildcard targets using filenames

Rules containing wildcards cannot be executed by rule name, because 
snakemake does not have enough information to fill in the wildcards.

However, you can run wildcard targets using filenames!

## Organizing your workflow with multiple concrete targets

You can provide multiple concrete target names that build specific sets of
files. This is useful when building or debugging your workflow.

@CTB: recipe with toplevel

## Advice on structuring your snakefile

* provide a default rule
* provide one or more concrete rules that are well named
* do not expect people (including yourself) to remember your filename layout
  or your rule names without documentation ;).

