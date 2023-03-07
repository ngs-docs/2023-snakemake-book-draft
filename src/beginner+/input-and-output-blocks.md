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
more comprehensively.

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
       echo {input}
       echo {output}
       touch {output}
   """
```

and when these are substituted into shell commands with `{input}` and
`{output}` they will be turned into space-separated lists in order,
i.e. the above shell command will print out first `file1.txt
file2.txt` and then `output1.txt output2.txt` before using `touch` to
create the empty output files.


- comma separated list + keywords
- wildcards can be used, no wildcards. prefix required
- shell quoting with :q

- lists
- names / namespaces

- flexibly rewrite command lines
- example: megahit

- just the basics, also have advanced section

recommendation:
- don't use list indices - either use {input} or {input.name}



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

