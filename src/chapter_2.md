# Chapter 2 - snakemake connects rules for you!

## Chaining rules with `input:` blocks

We can get snakemake to automatically connect rules by providing
information about the _input_ files a rule needs. Then, if you ask
snakemake to run a rule that requires certain inputs, it will
automatically figure out which rules produce those inputs as their
output, and automatically run them.

Let's add input information to the `plot_comparison` and `compare_genomes`
rules:

```python
{{#include ../code/section1/simple5.snakefile}}
```

Now you can just ask snakemake to run the last rule:
```shell
snakemake -j 1 plot_comparison
```
and snakemake will run the other rules only if those input files don't exist and need to be created.

## Taking a step back

The Snakefile is now a lot longer, but it's not _too_ much more complicated - what we've done is split the shell commands up into separate rules and annotated each rule with information  about what file it produces (the output), and what files it requires in order to run (the input).

This has the advantage of making it so you don't need to rerun commands unnecessarily. This is only a small advantage with our current workflow, because sourmash is pretty fast. But if each step takes an hour to run, avoiding unnecessary steps can make your work go much faster!

And, as you'll see later, these rules are reusable building blocks that can be incorporated into workflows that each produce different files. So there are other good reasons to break shell commands out into individual rules!

