# Beyond Your First Snakefile

This section is intended for people who have already used snakemake,
and now want to learn about and apply some more snakemake features!

## Some initial motivation

Let's consider the below Snakefile:

```python
{{#include ../code/examples/wildcards.fastqc/Snakefile:content}}
```

This Snakefile will find all files ending in `.fastq` under the
current directory. snakemake will then run FASTQC on each one, and
build a summary report using multiqc. It works for any number of
files, and will find files under any and all subdirectories. It can
run in parallel on a single machine, or on multiple machines on a
cluster, limited only by the computational resources you make
available to snakemake.  And if new FASTQ files are added, snakemake
will automatically detect them, run `fastqc` on them, and rerun
`multiqc` to update the summary report.

You might say that for all this power it is fairly short, as computer
programs go. But it is also somewhat terse and complicated looking!

This section is devoted to explaining all of the features of snakemake
(and how to write them into Snakefiles) that power the above functionality.
By the end of this section, you will be able to use 80% or more of the
core features of snakemake! And you will also have pointers into much of
the remaining 20% of snakemake's core feature set, which will be available
to you when and as you need it.

## A summary of this section

This section attempts to bridge between the more gradual on-ramp of the
first two sections, and the full power of this fully operational
workflow system as discussed in later sections as well as
[the official snakemake documentation](https://snakemake.readthedocs.io/).

This section introduces input and output blocks, wildcards, params
blocks, `glob_wildcards`, and `expand`. It will also discuss common
approaches to debugging snakemake workflows and cover basic syntax
rules.
