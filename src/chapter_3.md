# Chapter 3 - snakemake helps you avoid redundancy!

## Avoiding repeated filenames by using `{input}` and `{output}`

If you look at the previous Snakefile, you'll see a few repeated filenames - in particular, rule `compare_genomes` has three filenames in the input block and then repeats them in the shell block, and `compare.mat` is repeated several times in both `compare_genomes` and `plot_genomes`.

We can tell snakemake to reuse filenames by using `{input}` and `{output}`. The `{` and `}` tell snakemake to interpret these not as literal strings but as template variables that should be replaced with the value of `input` and `output`.

Let's give it a try!
```python
{{#include ../code/section1/simple6.snakefile}}
```

This approach not only involves less typing in the first place, but also makes it so that you only have to edit filenames in one place. This avoids mistakes caused by adding or changing filenames in one place and not another place - a mistake I've made plenty of times!

## snakemake makes it easy to rerun workflows!

It is common to want to rerun an entire workflow from scratch, to make sure that you're using the latest data files and software. Snakemake makes this easy!

You can ask snakemake to clean up all the files that it knows how to generate - and _only_ those files:
```shell
snakemake -j 1 plot_comparison --delete-all-output
```
which can then be followed by asking snakemake to regenerate the results:
```
snakemake -j 1 plot_comparison 
```

## snakemake will alert you to missing files if it can't make them!

Suppose you add a new file that does not exist to `compare_genomes`:

```python
{{#include ../code/section1/simple7.snakefile}}
```

Here, `does-not-exist.sig` doesn't exist, and we haven't given snakemake a rule to make it, either. What will snakemake do??

It will complain, loudly and clearly! And it will do so before running anything.

First, let's force the rule remove the output file that depends on the 
```shell
rm compare.mat
```

and then run `snakemake -j 1`. You should see:

```
Missing input files for rule compare_genomes:
    output: compare.mat
    affected files:
        does-not-exist.sig
```

This is exactly what you want - a clear indication of what is missing before your workflow runs.

# Next steps

We've introduced basic snakemake workflows, which give you a simple way to run shell commands in the right order. snakemake already offers a few nice improvements over running the shell commands by yourself or in a shell script -

* it doesn't run shell commands if you already have all the files you need
* it lets you avoid typing the same filenames over and over again
* it gives simple, clear errors when something fails

While this functionality is nice, there are many more things we can do to improve the efficiency of our bioinformatics!

In the next section, we'll explore 

- writing more generic rules using _wildcards_;
- typing fewer filenames by using more templates;
- providing a list of default output files to produce;
- running commands in parallel on a single computer
- loading lists of filenames from spreadsheets
- configuring workflows with input files
