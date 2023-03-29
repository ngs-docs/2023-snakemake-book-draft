# `input:` and `output:` blocks

As we saw in [Chapter 2](../chapter_2.md), snakemake will automatically
run rules for you when it detects that one rule provides an output
that is needed for another rule's input. And, in
[Chapter 3](../chapter_3.md), we saw that snakemake will fill in `{input}`
and `{output}` in the shell command based on the contents of the
`input:` and `output:` blocks. This becomes even more useful
with wildcards, as shown in [Chapter 6](../chapter_6.md), where wildcard
values are properly substituted into the `{input}` and `{output}` values.

In this chapter, we will discuss the use of input and output blocks
a bit more comprehensively.

## Providing inputs and outputs

As we saw previously, snakemake will happily take multiple input and
output values via comma-separated lists.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic}}
```

and when these are substituted into shell commands with `{input}` and
`{output}` they will be turned into space-separated lists in order,
i.e. the above shell command will print out first `file1.txt
file2.txt` and then `output file1.txt output file2.txt` before using `touch` to
create the empty output files.

Here we are also asking snakemake to quote filenames for the shell
command using `:q` - this means that if there are spaces, or
characters like quotes, they will be properly escaped using
[Python's shlex.quote function](https://docs.python.org/3/library/shlex.html#shlex.quote).
For example, here both output files contain a space, and so `touch
{output}` would create three files -- `output`, `file1.txt`, and
`file2.txt` -- rather than the correct two files, `output file1.txt`
and `output file2.txt`.  **This should always be used for anything
executed in a shell block** - it does no harm and it can prevent
serious bugs!

~~~admonish info title='Where can we (and should we) put commas?'

In the above code example, you will notice that `"file2.txt"` and
`"output file2.txt"` have commas after them:

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic}}
```

Are these required? **No.** The above code is equivalent to:

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic2}}
```

where there are no commas after the last line in input and output.

The general rule is this: you need internal commas to separate items
in the list, because otherwise strings will be concatenated to each
other - i.e. `"file1.txt" "file2.txt"` will become `"file1.txtfile2.txt"`,
even if there's a newline between them! But a trailing comma is optional
(and ignored).

Why!?  These are _Python tuples_ and you can add a trailing comma if
you like: `a, b, c,` is equivalent to `a, b, c`. You can read more
about that syntax [here](../appendix/python.md) (CTB link to specific
section).

So why do we add a trailing comma?! I suggest using trailing commas
because it makes it easy to add a new input or output without
forgetting to add a comma, and this is a mistake I make frequently!
This is a (small and simple but still useful) example of _defensive
programming_, where I use optional syntax rules to head off common
mistakes.

~~~

## Inputs and outputs are _ordered lists_

We can also refer to individual input and output entries by using
square brackets to index them as lists, starting with position 0:

```python
rule example:
   ...
   shell: """
       echo first input is {input[0]:q}
       echo second input is {input[1]:q}
       echo first output is {output[0]:q}
       echo second output is {output[1]:q}
       touch {output}
   """
```

but we don't recommend this: if you change the order of the inputs and
outputs, or add new inputs, you have to go through and adjust the
indices.  Relying on the number and position of indices in a list is
error prone!

## Using keywords for input and output files

You can instead name specific inputs and outputs using the _keyword_
syntax, and then refer to those using `input.` and `output.` prefixes:
```python
{{#include ../../code/examples/input_output.quoting/snakefile.names}}
```

Here, `a` and `b` in the input block, and `a` and `c` in the output block,
are keyword names for the input and output files; in the shell command,
they can be referred to with `{input.a}`, `{input.b}`, `{output.a}`, and
`{output.c}` respectively. Any valid variable name can be used, and the
same name can be used in the input and output blocks without collision,
as with `input.a` and `output.a`, above, which are distinct values.

**This is my recommended way of referring to specific input and output
files.** It is clearer to read, robust to rearrangements or additions, and
(perhaps most importantly) can guide the reader to the _purpose_ of each
input and output.

See below for an example of using this to run the megahit assembler.

(CTB discuss error message if you get name wrong)

## Example: writing a flexible command line

One example where it's particularly useful to be able to refer to
specific inputs is when running the `megahit` assembler on paired-end
input reads. Consider the following Snakefile:
```python
{{#include ../../code/examples/input_output.megahit/Snakefile:content}}
```
Here, we need to supply the input reads as two separate files,
with `-1` before one and `-2` before the second. The resulting
shell command is very readable!

## Input functions and more advanced features

There are a number of more advanced uses of input and output that rely
on Python programming - for example, one can define a Python function
that is called to generate a value based on a wildcard object, as below:

```python
{{#include ../../code/examples/input_output.quoting/snakefile.func:content}}
```

When asked to create `output5.txt`, this rule will look for
`file25.txt`.

Since this functionality relies on knowledge of
[wildcards](wildcards.md) as well as some knowledge of Python, we will
defer discussion of it until later!

## References and Links

* [Snakemake manual section on rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-and-rules)
