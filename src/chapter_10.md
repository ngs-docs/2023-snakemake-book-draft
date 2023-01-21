# Chapter 10 - using default rules

The last change we'll make the Snakefile for this section is
to add what's known as a default rule. What is this and why?

The 'why' is easier. Above, we've been careful to provide specific rule
names or filenames to snakemake, because otherwise it defaults to running
the first rule in the Snakefile. (There's no other way in which the order
of rules in the file matters - but snakemake will try to run the first
rule in the file if you don't give it a rule name or a filename on the
command line.)

This is less than great, because it's one more thing to remember and to
type. In general, it's better to have what's called a "default rule"
that lets you just run `snakemake -j 1` to generate the file or files you
want.

This is straightforward to do, but it involves a slightly different syntax -
a rule with _only_ an `input`, and no shell or output blocks. Here's
a default rule for our Snakefile that should be put in the file as
the first rule:

```python
rule all:
    input:
        "compare.mat.matrix.png"
```

What this rule says is, "I want the file `compare.mat.matrix.png`."
It doesn't give any instructions on how to do that - that's what the
rest of the rules in the file are! - and it doesn't _run_ anything,
because it has no shell block, and nor does it _create_ anything,
because it has no output block.

The logic here is simple, if not straightforward: this rule succeeds
when that input exists.

If you place that at the top of the Snakefile, then running
`snakemake -j 1` will produce `compare.mat.matrix.png`. You no
longer need to provide either a rule name or a filename on the command
line unless you want to do something _other_ than generate that file,
in which case whatever you put on the command line will ignore
the `rule all:`.

