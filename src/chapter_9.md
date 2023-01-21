# Chapter 9 - using `expand` to make filenames

You might note that the list of files in the `compare_genomes` rule
all share the same suffix, and they're all built using the same rule.
Can we use that in some way?

Yes! We can use a function called `expand(...)` and give it a template
filename to build, and a list of values to insert into that filename.

Below, we build a list of accessions named `ACCESSIONS`, and then use
`expand` to build the list of input files of the format `{acc}.fna.gz.sig`
from that list, creating one filename for each value in `ACCESSSIONS`.

```python
{{#include ../code/section2/interm5.snakefile}}
```

While wildcards and `expand` use the same syntax, they do quite different
things.

`expand` generates a list of filenames, based on a template and a list
of values to insert into the template. It is typically used to make a
list of files that you want snakemake to create for you.

Wildcards in rules provide the rules by which one or more files will
be actually created. They are recipes that say, "when you want to make
a file with name that looks like THIS, you can do so from files that
look like THAT, and here's what to run to make that happen.

`expand` tells snakemake WHAT you want to make, wildcard rules tell
snakemake HOW to make those things.

