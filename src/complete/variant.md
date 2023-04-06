# A complete variant calling example for a bacterial genome

Here, we provide a simple introductory variant calling workflow
for a bacterial genome. It assumes a haploid genome and it produces
both unfiltered and quality-filtered variant calls. The workflow
takes a single-ended read data set from the E. coli LTEE, and then:

* uses minimap2 to align the reads to a reference genome and produce a SAM file;
* converts the SAM file to a BAM file;
* sorts and indexes the BAM file;
* uses mpileup to generate a set of variant calls in a binary format;
* converts the binary format into a text VCF file;
* filters the calls based on coverage and quality.

## The complete Snakefile

TODO:
- add final version of Snakefile!

```python
<!-- cmdrun ../../scripts/remove-anchor.py ../../code/complete/variant/Snakefile -->
```

## The annotated Snakefile

### The download rules

* no input, only output
* curl retrieves files from the Web. useful for genome files etc. can use wget too.
* for a real workflow with your own data, you would probably omit these
  rules and instead save the data locally.
* -o {output} makes sure that the right filename is respected.

```python
{{#include ../../code/complete/variant/Snakefile:download}}
```

## Doing the initial mapping

```python
{{#include ../../code/complete/variant/Snakefile:mapping}}
```

## Converting SAM to BAM

* why do this separately rather than all in one?
  * error messages get conflated if you do too many things
  * good practice to separate things for parallel etc
* filtering of unmapped reads in first step, in addition to format conversion
* sort is more CPU intensive, could use multithreading here

```python
{{#include ../../code/complete/variant/Snakefile:sam_to_bam}}
```

## Calling variants

Refactor - too many things!
* split into three at least - gunzip, mpileup, call, view, filter?

Discuss:
* mpileup finds places with systematic differences
* call outputs them subject to some default parameters
* view converts bcf to vcf

```python
{{#include ../../code/complete/variant/Snakefile:call}}
```

## More TODO:

* add additional files!
* make this testable w/-n!
* make this testable w/big!
* remove test tags!
* how to interpret output/what to do
