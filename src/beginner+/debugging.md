# Techniques for debugging workflow execution (and fixing problems!)

* intermediate targets
* debug-dag
* logs
* print in Snakefile (use file=)
* finding and reading error messages - silence, killed, etc.
* the most common error messages - wildcards, output missing, input missing, whitespace/tabs etc
* using -n
* using -k
* running in single-CPU mode
* whitespace
* filling in wildcards

## A short check list

Summary: once you're done with syntax errors:

* run with `-n`
* run with `-j 1`
* run with `-p`
* run just the rules you're interested in (see [targets](targets.md))

## Finding, fixing, and avoiding syntax errors.

### Whitespace and indentation errors: finding, fixing, and avoiding them.

Use a good editor, e.g. vscode or some other text editor. Put it in snakemake
mode or Python mode (spaces etc.)

### Syntax errors, newlines, and quoting.

triple quotes vs single quotes

## Debugging Snakefile workflow declarations/specifications @@

### `MissingInputException`

One of the most common errors to encounter when writing a new workflow
is a `MissingInputException`. This is snakemake's way of saying three things:
first, it has figured out that it _needs_ a particular file; second,
that file does not already exist; and third,
it doesn't know how to _make_ that file (i.e. there's no rule that produces
that file).

For example, consider this very simple workflow file:
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.missing-input}}
```

When we run it, we get:
```
MissingInputException in rule example in file /Users/t/dev/2023-snakemake-book-draft/code/examples/errors.simple-fail/snakefile.missing-input, line 1:
Missing input files for rule example:
    affected files:
        file-does-not-exist
```

This error comes up in two common situations: either there is an input
file that you were supposed to provide the workflow but that is
missing (e.g. a missing FASTQ file); or the rule that is supposed to
produce this file (as an output) doesn't properly match.

### `MissingOutputException` and increasing `--latency-wait`

Sometimes you will see an error message that mentions a
`MissingOutputException` and suggests increasing the wait time with
`--latency-wait`.  This is most frequently a symptom of a rule that
does not properly create an expected output file.

For example, consider:
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.missing-output}}
```

Here we have a simple rule whose output block specifies that it will
create a file named `file-does-not-exist`, but (due to a typo in the
shell command) creates the wrong file instead. If we run this, we will
get the following message:

```
Waiting at most 5 seconds for missing files.
MissingOutputException in rule example in file /Users/t/dev/2023-snakemake-book-draft/code/examples/errors.simple-fail/snakefile.missing-output, line 3:
Job 0 completed successfully, but some output files are missing. Missing files after 5 seconds. This might be due to filesystem latency. If that is the case, consider to increase the wait time with --latency-wait:
file-does-not-exist
```

First, let's remember that the `output:` block is simply an
_annotation_, not a directive: it's telling snakemake what this rule
is _supposed_ to create, without actually creating it @@ (link to
input-output here).  The part of the rule that _creates_ the file is
typically the `shell:` block, and, here, we've made a mistake in the
shell block, and are creating the wrong file.

**There's no simple way for snakemake to know what files were actually
created by a shell block**, so snakemake doesn't try: it simple complains
that we _said_ running this rule would create a particular file, but
it _didn't_ create that file when we ran it. That's what
`MissingOutputException` generally means.

To fix this, we need to look at the shell command and understand why it is
not creating the desired file. That can get complicated, but one common
fix is to avoid writing filenames redundantly and instead use `{output}`
patterns in the shell block so that you don't accidentally use
different names in the `output:` block and in the `shell:` block.

So then what is this message about waiting 5 seconds for missing
files, and/or increasing `--latency-wait`? This refers to an advanced
situation (discussed @@later) that can occur when we are writing to a
shared network file system from jobs running on multiple machines. If
you're running snakemake on a single machine, this should never be a
problem! We'll defer discussion of this until later.

### `WorkflowError` and wildcards

Another common error is a `WorfklowError: Target rules may not contain
wildcards." This occurs when snakemake is asked to run a rule that contains
wildcards.

Consider:
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.missing-output}}
```

which generates:
```
WorkflowError:
Target rules may not contain wildcards. Please specify concrete files or a rule without wildcards at the command line, or have a rule without wildcards at the very top of your workflow (e.g. the typical "rule all" which just collects all results you want to generate in the end).
```

See [Using wildcards to generalize your rules](wildcards.md#all-wildcards-used-in-a-rule-must-match-to-wildcards-in-the-output-block) and [Targets](targets.md) for more information.

## Debugging running snakemake workflows 


## Run your rules once target at a time.

## Run your rules one job at a time.

## Finding and interpreting error messages

### Display of error messages for failed commands

## Running all the rules you can with `-k/--keep-going`

Snakemake has a slightly confusing presentation of error messages from
shell commands: the messages appear _above_ the notification that the
rule failed

Consider the following Snakefile:
```python
{{#include ../../code/examples/errors.simple-fail/snakefile.shell-fail}}
```

When you run this in a directory that does _not_ contain the file named `file-does-not-exist`, you will see the following output:

```
[Fri Apr 14 14:59:29 2023]                 
rule hello_fail:
    jobid: 0
    reason: Rules with neither input nor output files are always executed.
    resources: tmpdir=/var/folders/6s/_f373w1d6hdfjc2kjstq97s80000gp/T

ls: cannot access 'file-does-not-exist': No such file or directory
[Fri Apr 14 14:59:29 2023]
Error in rule hello_fail:
    jobid: 0
    shell:
        
        ls file-does-not-exist
    
        (one of the commands exited with non-zero exit code; note that snakemake uses bash strict mode!)
```

There are three parts to this output:

* the first part starts at `rule hello_fail:`, and declares that snakemake
  is going to run this rule, and gives the reason why.
  
* the second part contains the error message from running that
  command - here, `ls` fails because the file in question does not
  exist, and so it prints out `ls: cannot access
  'file-does-not-exist': No such file or directory `. **This is the error
  output by the failed command.**
  
* the third part starts at "Error in rule hello_fail" and describes the
  rule that failed: its name `hello_fail`, its jobid, and the shell command
  that was run (`ls file-does-not-exist`), together with some information
  about how the failure was detected (a non-zero exit code @@) and how the
  shell command was run (in so-called "strict mode" @@).
  
The somewhat non-intuitive part here is that the error message that is
specific to the failed rule - that the file in question did not exist -
appears _above_ the notification of failure.

There are some good reasons for this (@@ something to do about stdout capture)
and various ways to change this behavior (@@ logging) but, _by default_,
this is how snakemake reports errors in shell commands.

What this means in practice is that when you are debugging a failed
shell command, the place to look for the snakemake error is _above_
the notification of the failure!
  
@@ describe bash strict mode

@@ describe (briefly) logging

@@ when running with -j more than 1

### Out of memory errors: "Killed".

CTB: is it lowercase or uppercase?

Sometimes you will see a "rule failed" @@ error from snakemake, and
the only error message that you will be able to find is "killed".
What is this?

This generally means that your shell command (or shell process) was
terminated by an unavoidable signal from the operating system - and
the most common such signal is an out-of-memory error.

When a process uses too much memory, the default behavior of the
operating system is to _immediately_ terminate it - there's not much
else to be done.  Unfortunately, the default error message explaining this
is somewhat lacking.

There is no single way to _fix_ this problem, unfortunately. A few
general strategies include:

* switching to a system with more memory, or (if you are using a queuing
  system like slurm) requesting more memory for your job.
* if you are using a program that asks you to specify an amount of
  memory to use (e.g. some assemblers, or any java program), you can
  decrease the amount of memory you request on the command line.
* you can also decrease the size of the dataset you are using, perhaps
  by subdividing it or sub-sampling @@.
