# Chapter 4 - running rules in parallel

Let's take a look at the `sketch_genomes` rule from the last
`Snakefile` entry:

(@CTB note: Section 1 should be modified to have these explicit filenames
in there!)

```python
rule sketch_genomes:
    input:
        "genomes/GCF_000017325.1.fna.gz",
        "genomes/GCF_000020225.1.fna.gz",
        "genomes/GCF_000021665.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
        "GCF_000020225.1.fna.gz.sig",
        "GCF_000021665.1.fna.gz.sig"
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
```

This command works fine as it is, but it is _slightly_ awkward - because,
bioinformatics being bioinformatics, we are likely to want to add more
genomes into the comparison at some point, and right now each additional
genome is going to have to be added to both input and output.  It's not
a lot of work, but it's unnecessary.

Moreover, if add in a _lot_ of genomes, then this step could quickly
become a bottleneck. `sourmash sketch` may run quickly on 10 or 20 genomes,
but it will slow down if you give it 100 or 1000! (In fact, `sourmash sketch`
will actually take 100 times longer on 100 genomes than on 1.) Is there
a way to speed that up?

Yes - we can write a rule that can be run for each genome, and then
ask snakemake to run it in parallel for us!

Note: sometimes you have to have a single rule that deals with all of
the genomes - for example, `compare_genomes` has to compare _all_ the
genomes, and there's no simple way around that. But with `sketch_genomes`,
we do have a simple option!

Let's start by breaking this one rule into three _separate_ rules:

```python
rule sketch_genomes_1:
    input:
        "genomes/GCF_000017325.1.fna.gz",
    output:
        "GCF_000017325.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """

rule sketch_genomes_2:
    input:
        "genomes/GCF_000020225.1.fna.gz",
    output:
        "GCF_000020225.1.fna.gz.sig",
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """

rule sketch_genomes_3:
    input:
        "genomes/GCF_000021665.1.fna.gz",
    output:
        "GCF_000021665.1.fna.gz.sig"
    shell: """
        sourmash sketch dna -p k=31 {input} \
            --name-from-first
    """
    
# rest of Snakefile here!
```

It's wordy, but it will work - run:

```shell
snakemake -j 1 --delete-all plot_comparison
snakemake -j 1 plot_comparison
```

Before we modify the file further, let's enjoy the fruits of our labor:
we can now tell snakemake to run more than one rule at a time!

@CTB note: is there a way to ask snakemake to just rerun everything? force?

Try typing this:
```shell
snakemake -j 1 --delete-all plot_comparison
snakemake -j 3 plot_comparison
```

If you look closely, you should see that snakemake is running all three
`sourmash sketch dna` commands _at the same time_.

This is actually pretty cool and is one of the more powerful practical
features of snakemake: once you tell snakemake _what you want it to
do_ (by specifying targets) and give snakemake the set of recipes
telling it _how to do each step_, snakemake will figure out the
fastest way to run all the necessary steps with the resources you've given it.

In this case, we told snakemake that it could run up to three jobs at
a time, with `-j 3`. We could also have told it to run more jobs at a
time, but at the moment there are only three rules that can actually
be run at the same time - `sketch_genomes_1`, `sketch_genomes_2`, and
`sketch_genomes_3`. This is because the rule `compare_genomes` needs the
output of these three rules to run, and likewise `plot_genomes` needs
the output of `compare_genomes` to run. So they can't be run at the
same time as any other rules!

