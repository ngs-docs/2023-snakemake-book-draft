# Chapter 7 - giving snakemake filenames instead of rule names

Let's add a new genome into the mix, and start by generating a sketch
file (ending in `.sig`) for it.

Download the RefSeq assembly file (the `_genomic.fna.gz` file) for GCF_008423265.1 from [this NCBI link](https://www.ncbi.nlm.nih.gov/assembly/GCF_008423265.1), and put it in the `genomes/` subdirectory as `GCF_008423265.1.fna.gz`. (You can also download a saved copy with the right name from [this osf.io link](https://osf.io/7cdxn)).

Now, we'd like to build a sketch by running `sourmash sketch dna`
(via snakemake).

Do we need to add anything to the `Snakefile` to do this? No, no we don't!

To build a sketch for this new genome, you can just ask snakemake to make the
right filename like so:
```shell
snakemake -j 1 GCF_008423265.1.fna.gz.sig
```

Why does this work? It works because we have a generic wildcard rule for
building `.sig` files from files in `genomes/`!

When you ask snakemake to build that filename, it looks through all the
output blocks for its rules, and choose the rule with matching output -
importantly, this rule _can_ have wildcards, and if it does, it extracts
the wildcard from the filename!

## Warning: the `sketch_genome` rule has now changed!

As a side note, you can no longer ask snakemake to run the rule by its
name, `sketch_genome` - this is because the rule needs to fill in the
wildcard, and it can't know what `{accession}` should be without us
giving it the filename.

If you try running `snakemake -j 1 sketch_genome`, you'll get the following error:
>WorkflowError:
>Target rules may not contain wildcards. Please specify concrete files or a rule without wildcards at the command line, or have a rule without wildcards at the very top of your workflow (e.g. the typical "rule all" which just collects all results you want to generate in the end).

This is telling you that snakemake doesn't know how to fill in the wildcard
(and giving you some suggestions as to how you might do that, which we'll
explore below).

In this chapter we didn't need to modify the Snakefile at all to make use
of new functionality!

