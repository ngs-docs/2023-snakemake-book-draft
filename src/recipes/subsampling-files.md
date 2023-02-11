# Subsampling FASTQ files

In [Using wildcards to generalize your rules](./beginner+/wildcards.md),
we introduced the use of wildcards to generate 

```python
{{#include ../../code/examples/wildcards.subset/Snakefile}}
```

## Subsampling records rather than lines

Here, one potential problem is that we are producing subset files
based on the number of lines, not the number of records - typically,
in FASTQ files, four lines make a record. Ideally, the subset FASTQ file
produced by the recipe above would have the number of _records_ in its
filename, rather than the number of lines! However, this requires
multiplying the number of records by 4!

You can do this using [`params:` functions](./params-functions.md),
which let you introduce Python functions into your rules.
