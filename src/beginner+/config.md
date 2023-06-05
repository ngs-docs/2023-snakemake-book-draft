# Using configuration files

Configuration files are a snakemake feature that can be used to
separate the _rules_ in the workflow from the _configuration_ of the
workflow.  For example, suppose that we want to run the same sequence
trimming workflow on many different samples. With the techniques we've
seen so far, you'd need to change the Snakefile each time; with config
files, you can keep the Snakefile the same, and just provide a different
config file for each new sample. Config files can also be used to
define parameters, or override default parameters, for specific programs
being run by your workflow.

## A first example - running a rule with a single sample ID

Consider this Snakefile, which create an output file based on a
sample ID. Here the sample ID is taken from a config file and provided
via the Python dictionary named `config`:
```python
{{#include ../../code/examples/config.basic/snakefile.one_sample}}
```

The default configuration file is `config.one_sample.yml`, which
sets `config['sample']` to the value `XYZ_123`, and creates
`one_sample.XYZ_123.out`:
```yml
{{#include ../../code/examples/config.basic/config.one_sample.yml}}
```

However, the `configfile:` directive in the Snakefile can be overriden
on the command line by using `--configfile`; consider the file
`config.one_sample_b.yml`:
```yml
{{#include ../../code/examples/config.basic/config.one_sample_b.yml}}
```
If we now run `snakemake -s snakefile.one_sample --configfile
config.one_sample_b.yml -j 1`, the value of sample will be set to
`ABC_456`, and the file `one_sample.ABC_456.out` will be created.

(CTB: assert that the appropriate output files are created.)

## Specifying multiple sample IDs in a config file

The previous example only handles one sample at a time, but there's
no reason we couldn't provide multiple, using YAML lists. Consider
this Snakefile, `snakefile.multi_samples`:
```python
{{#include ../../code/examples/config.basic/snakefile.multi_samples}}
```

and this config file, `config.multi_samples.yml`:
```yml
{{#include ../../code/examples/config.basic/config.multi_samples.yml}}
```

Here, we're creating multiple output files, using a more complicated setup.

First, we use `samples` from the config file. The `config['samples']` value
is a Python list of strings, instead of a Python string, as in the previous
sample; that's because the config file specifies `samples` as a list in
the `config.multi_samples.yml` file.

Second, we switched to using [a wildcard rule](wildcards.md) in the
Snakefile, because we want to
[run one rule on many files](wildcards.md#running-one-rule-on-many-files);
this has a lot of benefits!

Last but not least, we provide a [default rule](../chapter_10.md) that
uses [the `expand` function with a single pattern and one list of values](expand.md#using-expand-with-a-single-pattern-and-one-list-of-values) to construct
the list of output files for the wildcard rule to make.

Now we can either edit the list of samples in the config file, or we can
provide different config files with different lists of samples!

## Specifying input spreadsheets via config file

## Specifying command line parameters in a config file

Config files aren't limited to sample IDs - you can put pretty much
anything in a config file.

Consider our `sourmash sketch` command from the workflow
we developed in [Section 1](../chapter_0.md), where we compare genomes
at a particular k-mer size. For example, from
[Chapter 2](../chapter_2.md), we have:

```python
rule sketch_genomes:
    output:
       "GCF_000017325.1.fna.gz.sig",
       "GCF_000020225.1.fna.gz.sig",
       "GCF_000021665.1.fna.gz.sig"
    shell: """
        sourmash sketch dna -p k=31 genomes/*.fna.gz --name-from-first
    """
```

Here, `sketch dna` is run with the parameter `-p k=31`, which sets the
k-mer size for comparison to k=31. This is a prime candidate for a
config file!

Using [a params block](params.md) and a config file, we could rewrite this
rule as 
```python
rule sketch_genomes:
    output:
       "GCF_000017325.1.fna.gz.sig",
       "GCF_000020225.1.fna.gz.sig",
       "GCF_000021665.1.fna.gz.sig",
    params:
        ksize=config['ksize'],
    shell: """
        sourmash sketch dna -p k={params.ksize} genomes/*.fna.gz --name-from-first
    """
```

This has a few nice features:

* the use of 'params' makes it clear to the reader that this is a parameter!
* the k-mer size is configurable!

CTB: check that it actually works with k=21!

CTB: talk about config.get and int/type validation

CTB: advanced usage: conditional parameters like output=pdf for compare.

note/danger, might want to have some info on parameters in output file names...

note/danger, talk about tradeoff b/t information in config file, vs information in snakefile - e.g. what programs to run, vs what parameters to use

## Debugging config files and displaying the `config` dictionary

I frequently want to know what the config actually is when running
snakemake. A convenient way to do this is to use `pprint` -
for example, see `snakefile.multi_samples.pprint`,
```python
{{#include ../../code/examples/config.basic/snakefile.multi_samples.pprint}}
```
which produces the following output:
```
config is:
{'samples': ['DEF_789', 'GHI_234', 'JKL_567']}
SAMPLES is:
['DEF_789', 'GHI_234', 'JKL_567']
```

CTB: explain python dict/list, or link.

CTB: link to debugging

CTB: talk about -n, and Python statements vs rules...

print, pprint
keys

using .get/providing defaults

## Advanced usage

### Providing config variables on the command line

You can also set individual config variables on the command line:

```
snakemake -j 1 -s snakefile.one_sample -C sample=ZZZ_123
```

CTB: how to do this for lists; how to do this for multiple config variables.

### Providing multiple config files

`--configfiles`

## Recap

With config files, you can:

* separate configuration from your workflow
* provide multiple different config files for the same workflow
* change the samples by editing a YML file instead of a Snakefile
* make it easy to validate your input configuration (DISCUSS)

## Leftovers

* Point to official snakemake docs
* Guide to YAML and JSON syntax
