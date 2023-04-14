# Chapter 11 - our final Snakefile - review and discussion

Here's the final Snakefile for comparing four genomes.

This snakemake workflow has the following features:

* it has a single list of accessions at the top of the Snakefile, so
  that more genomes can be added by changing only one place in the
  file. See
  [Using `expand` with a single pattern and one list of values](../beginner+/expand.md#using-expand-with-a-single-pattern-and-one-list-of-values)
  for more discussion of this.
  
* the workflow uses a default rule `all`, a "pseudo-rule" that
  contains only input files. This is the default rule that snakemake
  will run if executed without any targets on the command line. See
  [Running rules and choosing targets from the command line](./beginner+/targets.md)
  for some discussion of targets and Snakefile organization.
  
* the workflow uses one wildcard rule, `sketch_genome`, to convert
  _multiple_ genome files ending in `.fna.gz` into sourmash signature files.
  See [Using wildcards to generalize your rules](./beginner+/wildcards.md) for
  discussion of wildcards.
  
* there is also a rule `compare_genomes` that uses `expand` to
  construct the complete list of genomes signature needed to run
  `sourmash compare`.  Again, see
  [using `expand` with a single pattern and one list of values](../beginner+/expand.md#using-expand-with-a-single-pattern-and-one-list-of-values)
  for more discussion of this.
  
* the last rule, `plot_comparison`, takes the output of `compare_genomes`
  and turns it into a PNG image via `sourmash plot` via the provided
  shell command.

```python
{{#include ../code/section2/interm6.snakefile}}
```

In the following sections we will cover the core features of snakemake
used in this Snakefile more thoroughly, and then introduce some more
complex bioinformatics workflows as well as a number of useful
patterns and reusable recipes.
