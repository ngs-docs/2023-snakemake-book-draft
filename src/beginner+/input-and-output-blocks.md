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

## Providing lists

As we saw previously, snakemake will happily take multiple input and
output values via comma-separated lists.

```python
rule example:
   input:
       "file1.txt",
       "file2.txt",
   output:
       "output1.txt",
       "output2.txt"
   shell: """
       echo {input:q}
       echo {output:q}
       touch {output:q}
   """
```

and when these are substituted into shell commands with `{input}` and
`{output}` they will be turned into space-separated lists in order,
i.e. the above shell command will print out first `file1.txt
file2.txt` and then `output1.txt output2.txt` before using `touch` to
create the empty output files.

Here we are also asking snakemake's templating minilanguage (CTB link)
to quote them for the shell - this means that if there are spaces, or
characters like quotes, they will be properly escaped using
[Python's shlex.quote function](https://docs.python.org/3/library/shlex.html#shlex.quote).
(CTB some examples - whitespace, and quotes?) **This should always be
used for anything executed in a shell block** - it does no harm and it
can prevent serious bugs!

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

but we don't recommend this, because if you change the order of the
inputs and outputs, or add some, you have to go through and adjust the
indices.

## Using keywords for input and output files

You can also use keywords to name

```python
rule example:
   input:
       a="file1.txt",
       b="file2.txt",
   output:
       a="output1.txt",
       c="output2.txt"
   shell: """
       echo first input is {input.a:q}
       echo second input is {input.b:q}
       echo first output is {output.a:q}
       echo second output is {output.c:q}
       touch {output}
   """
```

Here, `a` and `b` in the input block, and `a` and `c` in the output block,
are keyword names for the input and output files; and in the shell command,
they can be referred to with `{input.a}`, `{input.b}`, `{output.a}`, and
`{output.c}` respectively. Any valid variable name can be used.

**This is my recommended way of referring to specific input and output
files.** It is clearer to read, and robust to rearrangements or additions.

See below for an example of using this to run the megahit assembler.

(CTB discuss error message if you get name wrong)

## Examples

- wildcards can be used, no wildcards. prefix required
- example: megahit
- flexibly rewrite command lines

## Input functions and more advanced features

There are a number of more advanced uses of input and output that rely
on Python programming - for example, one can define a Python function
that is called to generate a value based on a wildcard object, as below:

```python
def multiply_by_5(w):
    return f"file{int(w.val) * 5}.txt"
    
    
rule make_file:
    input:
        filename=multiply_by_5,
    output:
        "output{val}.txt"
    shell: """
        cp {input} {output}
    """
```

When asked to create `output5.txt`, this rule will look for
`file25.txt`.

Since this functionality relies on some knowledge of Python, we will
defer discussion of it until later.

## References and Links

[Python minilanguage format](https://docs.python.org/3/library/string.html#formatspec)

[Snakemake manual section](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-and-rules)
