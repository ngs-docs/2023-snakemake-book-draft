# Using wildcards to generalize your rules

As we showed in [Chapter 6](../chapter_6.md), when you have repeated
substrings between input and output, you can extract them into
wildcards - going from a rule that makes specific outputs from
specific inputs into rules that operate on any input/output sets that
match a pattern.

For example, the following code creates a single sourmash sketch
from a specific genome:

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

While this rule does the same for *any* genome ending in `.fna.gz`!

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

Here, `{accession}` is a wildcard that "fills in" as needed for any filename
that is under the `genomes/` directory and ends with `.fna.gz`.

Snakemake uses simple _pattern matching_ to determine the value of
`{accession}` - if asked for a filename ending in `.fna.gz.sig`, snakemake
takes the prefix, and then looks for the matching input file
`genomes/{accession}.fna.gz`, and fills in `{input}` accordingly.

Wildcards are incredibly useful and using them means that in many
cases you can write a single rule that can generate hundreds or
thousands of files! However, there are a few subtleties to consider. In
this chapter, we're going to cover the most important of those
subtleties, and provide links where you can learn more.

## Rules for wildcards

First, let's go through some basic rules for wildcards.

### Wildcards are determined by the desired output

The first and most important rule of wildcards is this: snakemake
fills in wildcard values based on the filename it is asked to produce.

Consider the following rule:

```python
{{#include ../../code/examples/wildcards.output/snakefile.output}}
```
The wildcard in the output block will match _any_ file that ends with
`.a.out`, and the associated shell command will create it!  This is both
powerful and constraining: you can create any file with the suffix
`.a.out` - but you also need to _ask_ for the file to be created.

This means that in order to make use of this rule, there needs to be
another rule that has a file that ends in `.a.out` as a required
input.  (You can also explicitly ask for such a file on the command
line. CTB doc link.)  There's no other way for snakemake to guess at
the value of the wildcard: snakemake follows the dictum that explicit
is better than implicit, and it will not guess at what files you want
created.

For example, the above rule could be paired with another rule that asks
for one or more filenames ending in `.a.out`:
```python
rule make_me_a_file:
    input:
        "result1.a.out",
        "result2.a.out",
```

This also means that once you put a wildcard in a
rule, you can no longer run that rule by the rule name - you have to
ask for a filename, instead.  If you try to run a rule that contains a
wildcard but don't tell it what filename you want to create, you'll get:
```
Target rules may not contain wildcards.
```

One common way to work with wildcard rules is to have another rule that
uses `expand` to construct a list of desired files; this is often paired
with a `glob_wildcards` to load a list of wildcards. See the recipe for
renaming files by prefix, below, or the chapter on
[Using `expand` to generate filenames](expand.md).

### All wildcards used in a rule must match to wildcards in the `output:` block

snakemake uses the wildcards in the `output:` block to fill in the wildcards
elsewhere in the rule, so you can only use wildcards mentioned in one or
more outputs.

This means that every wildcard used in the `input:` block needs to be
present in `output:`.  Consider the following example, where the input
block contains a wildcard `analysis` that is not used in the output
block:

```python
# this does not work:

rule analyze_sample:
    input: "{sample}.x.{analysis}.in"
    output: "{sample}.out"
```

This doesn't work because snakemake doesn't know how to fill in the
`analysis` wildcard in the _input_ block, and you will get an error
that says so:
```
WildcardError in line 1 of ...
Wildcards in input files cannot be determined from output files:
'analysis'
```

Think about it this way: if this worked, there could be multiple
different input files for the same output, and snakemake would
have no way to choose which input file to use to produce the
desired output; moreover, the outputs would presumably be different
depending on the inputs used, leading to irreproducibility.

Every wildcard in the `input:` block does need to be in the `output:`
block.  However, there are situations where wildcards in the `output:`
block do _not_ need to be in the `input:` block - see "Using wildcards
to determine parameters to use in the shell block", below, on using
wildcards to determine parameters for the shell block!

### Wildcards are local to each rule

Wildcard names only need to match _within_ a rule block; wildcards are not
shared between rules. You _can_ use the same
wildcard names in multiple rules for consistency and readability, but
snakemake will treat them as independent wildcards, and wildcard values
will not be shared.

So, for example, these two rules use the same wildcard `a` in both rules -

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{a}.second.txt"
    output: "{a}.third.txt"
```

but this is equivalent to these next two rules, which use _different_
wildcards `a` and `b` in the separate rules:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"

rule analyze_that:
    input: "{b}.second.txt"
    #        ^-- different - 'b' instead of 'a' in the first rule
    output: "{b}.third.txt"
    #        ^-- different - 'b' instead of 'a' in the first rule
```

There is one exception to the rule that wildcards are independent:
when you use 
[global wildcard constraints](../reference/wildcard-constraints.md) to
limit wildcard matching by wildcard name, the constraints
apply across all uses of that wildcard name in the Snakefile.
However, the _values_ of the wildcards remain independent - it's just
the constraint that is shared by all wildcards of the same name.

<!-- CTB: fix link to point directly to global wildcard constraints. -->

While wildcards are independent in values and you could use different
wildcards in every rule, it is a good convention to choose wildcards
to have the same semantic meaning across the Snakefile - e.g. always
use `sample` consistently to refer to a sample identifier, or `accession` to
refer to a database ID. This makes reading the
Snakefile easier!

One interesting addendum: because wildcards are local to each rule, you
are free to match different parts of patterns in different rules!
See "Mixing and matching wildcards", below.

### The wildcard namespace is implicitly available in `input:` and `output:` blocks, but not in other blocks.
    
Within the `input:` and `output:` blocks in a rule, you can refer to
wildcards directly by name. If you want to use wildcards in most other
parts of a rule you need to use the `wildcards` prefix; the only
exception to this rule is `params:` blocks (see the chapter
[`params:` blocks and `{params}`](params-blocks.md)). Here, `wildcards`
is a _namespace_, which we will talk about more later. (CTB)

Consider this Snakefile:

```python
# this does not work:

rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {a}"
```

Here you will get an error,
```
NameError: The name 'a' is unknown in this context. Did you mean 'wildcards.a'?
```

As the error suggests, you need to use `wildcards.a` in
the shell block instead:

```python
rule analyze_this:
    input: "{a}.first.txt"
    output: "{a}.second.txt"
    shell: "analyze {input} -o {output} --title {wildcards.a}"
```

### Wildcards match as broadly as possible, unless constrained in some way

Wildcard pattern matching chooses the _longest possible_ match to
_any_ characters, which can result in slightly confusing
behavior. Consider:

```python
{{#include ../../code/examples/wildcards.greedy/snakefile.1}}
```

In the `something` rule, for the desired output file `x.y.z.gz`,
`{prefix}` will currently be `x.y` and `{suffix}` will be `z`.
But it would be equally valid for `{prefix}` to be `x` and
suffix to be `y.z`.

A more extreme example shows the greedy matching even more clearly:
```python
{{#include ../../code/examples/wildcards.greedy/snakefile.2}}
```
where `{suffix}` is reduced down to a single character, `e`, and
`{prefix}` is `longer_filenam`!

Two simple rules for wildcard matching are:
* all wildcards must match at least one character.
* after that, wildcards will match _greedily_: each wildcard will match everything it can before the next wildcard is considered.

This is why it's good practice to use
[wildcard constraints](../reference/wildcard-constraints.md) to limit
wildcard matching.  See "Constraining wildcards to avoid
subdirectories and/or periods", below, for some examples, and see the
[wildcard constraints](../reference/wildcard-constraints.md) chapter
for more details!

## Some examples of wildcards

### Running one rule on many files

Wildcards can be used to run the same simple rule on many files - this is
one of the simplest and most powerful uses for snakemake!

Consider this Snakefile for compressing many files:

```python
{{#include ../../code/examples/wildcards.many/Snakefile}}
```

This Snakefile specifies a list of compressed files that it wants produced,
and relies on wildcards to do the pattern matching required to find the
input files and fill in the shell block.

See [Replacing for loops with Snakefiles](../recipes/replacing-for.md)
for more examples of this powerful pattern!

That having been said, this Snakefile is inconvenient to write and is
somewhat error prone:

* writing out the files individually is annoying if you have many of them!
* to generate the list of files, you have to hand-rename them, which is
  error prone!
  
Snakemake provides several features that can help with these issues. You
can load the list of files from a text file or spreadsheet, or get the
list directly from the directory using `glob_wildcards`; and you can
use `expand` to rename them in bulk. Read on for some examples!

```admonish info title='Why is this better than using gzip directly?'

It is possible to accomplish the same task by using `gzip -k original/*`,
although you'd have to move the files into their final location, too.

How is using `gzip -k original/*` different from using snakemake? And
is it better?

First, while the results aren't different - both approaches will
compress the set of input files, which is what you want! - the `gzip
-k` command runs in *serial* and will not run in *parallel* - that is,
gzip will by default compress one file at a time. The Snakefile will
run the rule `gzip_file` _in parallel_, using as many processors as you
specify with `-j`.  That means that if you had many, many such files -
a common problem in bioinformatics! - the snakemake version could
potentially run many times faster.

Second, specifying many files on the command line with `gzip -k
original/*` works with `gzip` but not with every shell command. Some
commands only run on one file at a time; `gzip` just happens to work
whether you give it one or many files. Many other programs do not work
on multiple input files; e.g. the `fastp` program for preprocessing
FASTQ files runs on one dataset at a time.  (It's also worth
mentioning that snakemake gives you a way to flexibly write custom
command lines; for some examples, see the chapter on
[Input and Output Blocks](input-and-output-blocks.md).)

Third, in the Snakefile we are being explicit about which files we
expect to exist after the rules are run, while if we just ran `gzip -k
original/*` we are asking the shell to compress every file in
`original/`. If we accidentally deleted a file in the `original`
subdirectory, then gzip would not know about it and would not
complain - but snakemake would. This is a theme that will come up
repeatedly - it's often safer to be really explicit about what files
you expect, so that you can be alerted to possible mistakes.

And, fourth, the Snakefile approach will let you rename the output
files in interesting ways - with `gzip -k original/*`, you're stuck
with the original filenames.  This is a feature we will explore in the
next subsection!
```

### Renaming files by prefix using `glob_wildcards`

Consider a set of files named like so:

```
F3D141_S207_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq
```
within the `original/` subdirectory.

Now suppose you want to rename them all to get rid of the `_001` suffix
before `.fastq`. This is very easy with wildcards!

The below Snakefile uses `glob_wildcards` to load in a list of files from
a directory and then make a copy of them with the new name under the
`renamed/` subdirectory. Here, `glob_wildcards` extracts the `{sample}`
pattern _from_ the set of available files in the directory:

```python
{{#include ../../code/examples/wildcards.renaming_simple/Snakefile}}
```

This Snakefile also makes use of `expand` to rewrite the loaded list
into the desired set of filenames. This means that we no
longer have to write out the list of files ourselves - we can let
snakemake do it! `expand` is discussed further in
[Using expand to generate filenames](expand.md).

Note that here you could do a `mv` instead of a `cp` and then
`glob_wildcards` would no longer pick up the changed files after
running.

This Snakefile loads the list of files from the directory itself,
which means that if an input file is accidentally deleted, snakemake
won't complain. When renaming files, this is unlikely to cause
problems; however, when running workflows, we recommend loading the
list of samples from a text file or spreadsheet to avoid problems

<!-- (CTB point to a recipe). -->

Also note that this Snakefile will find and rename all files in
`original/` as well as any subdirectories! This is because
`glob_wildcards` by default includes all subdirectories. See
the next section below to see how to use wildcard constraints to
prevent loading from subdirectories.

### Constraining wildcards to avoid subdirectories and/or periods

Wildcards match to any string, including '/', and so `glob_wildcards`
will automatically find files in subdirectories and will also "stretch
out" to match common delimiters in filenames such as '.' and '-'. This
is commonly referred to as "greedy matching" and it means that
sometimes your wildcards will match to far more of a filename than you
want!  You can limit wildcard matches using wildcard constraints.

Two common wildcard constraints are shown below, separately and in
combination.  The first constraint avoids files in subdirectories, and
the second constraint avoids periods.

```python
{{#include ../../code/examples/wildcards.basic_constrain/Snakefile:constraints}}
```

See [Wildcard constraints](../reference/wildcard-constraints.md) for more
information and details.

## Advanced wildcard examples

### Renaming files using multiple wildcards

The first renaming example above works really well when you want to change just
the suffix of a file and can use a single wildcard, but if you want to
do more complicated renaming you may have to use multiple wildcards.

Consider the situation where you want to rename files from the form of
`F3D141_S207_L001_R1_001.fastq` to `F3D141_S207_R1.fastq`. You can't
do that with a single wildcard, unfortunately - but you can use two,
like so:


```python
{{#include ../../code/examples/wildcards.renaming/Snakefile}}
```

We're making use of three new features in this code:

First, `glob_wildcards` is matching multiple wildcards, and
puts the resulting values into a single result variable (here, `files`).

Second, the matching values are placed in two ordered lists,
`files.sample` and `files.r`, such that values extracted from file names
match in pairs.

Third, when we use `expand`, we're asking it to "zip" the two lists of
wildcards together, rather than the default, which is to make all
possible combinations with `product`.  See
[Using expand to generate filenames](expand.md) for more information
on `zip` vs `product`.

Also - as with the previous example, this Snakefile will find and
rename all files in `original/` as well as any subdirectories!

Links:

* [snakemake documentation on using zip instead of product](https://snakemake.readthedocs.io/en/stable/project_info/faq.html#i-don-t-want-expand-to-use-the-product-of-every-wildcard-what-can-i-do)

### Mixing and matching strings

A somewhat nonintuitive (but also very useful) consequence of wildcards
being local to rules is that you can do clever string matching to mix and
match generic rules with more specific rules.

Consider this Snakefile, in which we are mapping reads from multiple
samples to multiple references (rule `map_reads_to_reference`) as well
as converting SAM to BAM files:

<!-- CTB: transfer to functional Snakefile? -->

```python
rule all:
    input:
        "sample1.x.ecoli.bam",
        "sample2.x.shewanella.bam",
        "sample1.x.shewanella.bam"

rule map_reads_to_reference:
    input:
        reads="{sample}.fq",
        reference="{genome}.fa",
    output:
        "{reads}.x.{reference}.sam"
    shell: "minimap2 -ax sr {input.reference} {input.reads} > {output}"
        
rule convert_sam_to_bam:
    input:
        "{filename}.sam"
    output:
        "{filename}.bam"
    shell: "samtools view -b {input} -o {output}
```

Here, snakemake is happily using different wildcards in each rule, and
matching them to different parts of the pattern! So,

* Rule `convert_sam_to_bam` will generically convert any SAM file to a BAM
file based solely on the `.bam` and `.sam` suffixes.

* However, `map_reads_to_references` will only produce mapping files that
match the pattern of `{sample}.x.{reference}`, which in turn depend on the
existence of  `{reference}.fa` and `{sample}.fastq`.

This works because, ultimately, snakemake is just matching strings
and does not "know" anything about the structure of the strings that
it's matching. And it also doesn't remember wildcards across rules. So
snakemake will happily match one set of wildcards in one rule, and a
different set of wildcards in another rule!

### Using wildcards to determine parameters to use in the shell block.

You can also use wildcards to build rules that produce output files
where the parameters used to _generate_ the contents are based on the
filename; for example, consider this example of generating subsets
of FASTQ files:

```python
{{#include ../../code/examples/wildcards.subset/Snakefile}}
```

Here, the wildcard is _only_ in the output filename, not in the
input filename. The wildcard value is used by snakemake to determine
how to fill in the number of lines for `head` to select from the file!

This can be really useful for generating files from giving many different
parameters to a shell command - what we call "parameter sweeps".  More
about this later!

<!-- See CTB XXX.

CTB link to:
* params functions, params lambda?
* parameter sweeps with this and expand
-->

## How to think about wildcards

Wildcards (together with `expand` and `glob_wildcards`) are among
the most powerful and useful features in snakemake: they permit generic
application of rules to an arbitrary number of files, based entirely
on simple patterns.

However, with that power comes quite a bit of complexity!

Ultimately, wildcards are all about *strings* and *patterns*.
Snakemake is using pattern matching to extract patterns from the
desired output files, and then filling those matches in elsewhere in
the rule. Most of the ensuing complexity comes avoiding ambiguity in
matching and filling in patterns, along with the paired challenge of
constructing all the names of the files you actually want to create.

## Additional references

See also: the
[snakemake docs on wildcards](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-wildcards).
