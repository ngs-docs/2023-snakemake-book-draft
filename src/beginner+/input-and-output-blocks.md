# `input:` and `output:` blocks

@@ make a note somewhere that these are annotations, not directives,
and that's why we suggest using `{output}`.

@@ make a note saying that if it wants one output, it will run the rule.

As we saw in [Chapter 2](../chapter_2.md), snakemake will automatically
"chain" rules by connecting inputs to outputs. That is, snakemake
will figure out _what to run_ in order to produce the desired output,
even if it takes many steps.

In [Chapter 3](../chapter_3.md), we also saw that snakemake will fill
in `{input}` and `{output}` in the shell command based on the contents
of the `input:` and `output:` blocks. This becomes even more useful
when using wildcards to generalize rules, as shown in
[Chapter 6](../chapter_6.md), where wildcard values are properly
substituted into the `{input}` and `{output}` values.

Input and output blocks are key components of snakemake workflows.
In this chapter, we will discuss the use of input and output blocks
a bit more comprehensively.

## Providing inputs and outputs

As we saw previously, snakemake will happily take multiple input and
output values via comma-separated lists and substitute them into strings
in shell blocks.

```python
{{#include ../../code/examples/input_output.quoting/snakefile.basic}}
```

When these are substituted into shell commands with `{input}` and
`{output}` they will be turned into space-separated ordered lists:
e.g. the above shell command will print out first `file1.txt
file2.txt` and then `output file1.txt output file2.txt` before using `touch` to
create the empty output files.

In this example we are also asking snakemake to quote filenames for
the shell command using `:q` - this means that if there are spaces,
characters like single or double quotation marks, or other characters
with special meaning they will be properly escaped using
[Python's shlex.quote function](https://docs.python.org/3/library/shlex.html#shlex.quote).
For example, here both output files contain a space, and so `touch
{output}` would create three files -- `output`, `file1.txt`, and
`file2.txt` -- rather than the correct two files, `output file1.txt`
and `output file2.txt`.

**Quoting filenames with `{...:q}` should always be used for anything
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
even if there's a newline between them! But a comma trailing after the
last filename is optional (and ignored).

Why!?  These are _Python tuples_ and you can add a trailing comma if
you like: `a, b, c,` is equivalent to `a, b, c`. You can read more
about that syntax [here](../appendix/python.md) (CTB link to specific
section).

So why do we add a trailing comma?! I suggest using trailing commas
because it makes it easy to add a new input or output without
forgetting to add a comma, and this is a mistake I make frequently!
This is a (small and simple but still useful) example of _defensive
programming_, where we can use optional syntax rules to head off common
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

However, **we don't recommend this** because it's fragile. If you
change the order of the inputs and outputs, or add new inputs, you
have to go through and adjust the indices to match.  Relying on the
number and position of indices in a list is error prone and will make
your Snakefile harder to change later on!

## Using keywords for input and output files

You can also name specific inputs and outputs using the _keyword_
syntax, and then refer to those using `input.` and `output.` prefixes.
The following Snakefile rule does this:
```python
{{#include ../../code/examples/input_output.quoting/snakefile.names}}
```

Here, `a` and `b` in the input block, and `a` and `c` in the output block,
are keyword names for the input and output files; in the shell command,
they can be referred to with `{input.a}`, `{input.b}`, `{output.a}`, and
`{output.c}` respectively. Any valid variable name can be used, and the
same name can be used in the input and output blocks without collision,
as with `input.a` and `output.a`, above, which are distinct values.

**This is our recommended way of referring to specific input and
output files.** It is clearer to read, robust to rearrangements or
additions, and (perhaps most importantly) can help guide the reader
(including "future you") to the _purpose_ of each input and output.

If you use the wrong keyword names in your shell code, you'll get an
error message. For example, this code:
```python
{{#include ../../code/examples/input_output.quoting/snakefile.names.broken:content}}
```
gives this error message:
```
AttributeError: 'InputFiles' object has no attribute 'z', when formatting the following:

       echo first input is {input.z:q}
   
```

## Example: writing a flexible command line

One example where it's particularly useful to be able to refer to
specific inputs is when running programs on files where the input
filenames need to be specified as optional arguments.  One such
program is the `megahit` assembler when it runs on paired-end input
reads. Consider the following Snakefile:

```python
{{#include ../../code/examples/input_output.megahit/Snakefile:content}}
```

In the shell command here, we need to supply the input reads as two
separate files, with `-1` before one and `-2` before the second. As a
bonus the resulting shell command is very readable!

## Input functions and more advanced features

There are a number of more advanced uses of input and output that rely
on Python programming - for example, one can define a Python function
that is called to _generate_ a value dynamically, as below -

```python
{{#include ../../code/examples/input_output.quoting/snakefile.func:content}}
```

When asked to create `output5.txt`, this rule will look for
`file25.txt` as an input.

Since this functionality relies on knowledge of
[wildcards](wildcards.md) as well as some knowledge of Python, we will
defer discussion of it until later!

## References and Links

* [Snakemake manual section on rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-and-rules)
