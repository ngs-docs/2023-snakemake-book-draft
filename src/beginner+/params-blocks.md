# `params:` blocks and `{params}`

As we saw previously,
[input and output blocks](input-and-output-blocks.md) are key to the
way snakemake works: they let snakemake automatically connect rules
based on the inputs necessary to create the desired output. However,
input and output blocks are limited in certain ways: most specifically,
every entry in both input and output blocks _must_ be a filename.
And, because of the way snakemake works, the filenames specified in
the input and output blocks must exist in order for the workflow to
proceed past that rule.

Frequently, shell commands need to take parameters other than
filenames, and these parameters may be values that can or should be
calculated by snakemake.  Therefore, snakemake also supports a
`params:` block that can be used to provide strings that are _not_
filenames in the shell block, colloquially known as parameters. As
you'll see below, these can be used for a variety of purposes,
including user-configurable parameters as well as parameters that can
be calculated automatically by Python code.

## A simple example of a params block

Consider:
```python
{{#include ../../code/examples/params.basic/snakefile.params}}
```

Here, the value `5` is assigned to the name `val` in the `params:` block,
and is then available under the name `{params.val}` in the `shell:` block.
This is analogous to [using keywords in input and output blocks](input-and-output-blocks.md#using-keywords-for-input-and-output-files), but unlike in
input and output blocks, keywords _must_ be used in params blocks.

In this example, there's no gain in functionality, but there is some
gain in readability: the syntax makes it clear that `val` is a tunable
parameter that can be modified without understanding the details of
the shell block.

## Params blocks have access to wildcards

Just like the `input:` and `output:` blocks, wildcard values are
directly available in `params:` blocks without using the `wildcards`
prefix; for example, this means that you can use them in strings with
the standard [string formatting operations](string-formatting.md).

This is useful when a shell command needs to use something other than
the filename - for example, the `bowtie` read alignment software takes
the _prefix_ of the output SAM file via `-S`, which means you cannot
name the file correctly with `bowtie ... -S {output}`.  Instead, you
could use `{params.prefix}` like so:
```python
{{#include ../../code/examples/params.basic/snakefile.params_wildcards:content}}
```
If you were to use `-S {output}` here, you would end up producing a file
`reads.sam.sam`!

## Params blocks also support a variety of other functionality

CTB

* bring in config values
* [input functions & params functions](../recipes/params-functions.md)
* use comma-separated value for megahit as example? e.g. -r 1,2,3

## Links and references:

* Snakemake docs: [non-file parameters for rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#non-file-parameters-for-rules)
