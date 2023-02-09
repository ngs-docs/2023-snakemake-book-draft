# Using wildcards to generalize your rules

As in [Chapter 6](../chapter_6.md), when you have repeated substrings between
input and output, you can extract them into wildcards - going from

```python
rule sketch_genomes_1:
    input:
        "genomes/GCF_000017325.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} --name-from-first
    """
```

to

```python
rule sketch_genomes_1:
    input:
        "genomes/{accession}.fna.gz",
    output:
        "{accession}.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
```

In this simple (and very common!) case, wildcards do something very
straightforward: snakemake uses pattern matching to see whether, when
missing a desired output (here a filename ending in `.fna.gz.sig`),
there is a corresponding input file; and if so, it runs the associated
shell command.

This is incredibly useful and means that in many cases you can write
a single rule that is applied to hundreds or thousands of files!

As usual, however, there are a lot of subleties to consider. In this
chapter, we're going to cover the most important of those subtleties, and
provide links where you can learn more.

## Rules for wildcards

### Wildcards are local to each rule

Wildcard names only match within a rule.

Use `wildcards.` to access them.

As a corollary, you can mix and match wildcards.

### All wildcards in the `output:` must match to wildcards in `input:`

Thought experiment: consider a wildcard in input that is unused in output.

### Wildcards match greedily, unless constrained

## Some examples of wildcards


### Renaming files

https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do

* renaming files



```
F3D141_S207_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq
```


```python
rule rename:
    input:
        "{sample}_L001_{r}_001.fastq",
    output:
        "{sample}_{r}.fastq"
```

* mixing/matching strings

* constraining wildcards to avoid (e.g.) subdirectories

Mention:

* all wildcards in output must match to wildcards in input
* wildcards only make sense within rules, with a few exceptions
* here, snakemake is constructing strings to run, that is all.
* snakemake only knows about strings, noting else
* directories / etc
* simple renaming foo
* namespaces, within rules vs outside of rules
* wildcard constraints
* pair vs metagenome/genome - jean setup.
