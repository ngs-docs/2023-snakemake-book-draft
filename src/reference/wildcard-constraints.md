# Limiting wildcard matching with wildcard constraints

Wildcards are one of the most powerful features in snakemake. But sometimes
they cause trouble by matching too broadly, to too many files!

See the [section on wildcards](../beginner+/wildcards.md) for an introduction
to wildcards!

By default, wildcards in snakemake match to one or more characters -
that is, they won't match to an empty string, but they'll match to
_anything else_. As discussed in the wildcards chapter, this can
cause problems!

snakemake supports limiting wildcard matching with a feature called
[wildcard constraints](https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#constraining-wildcards). Wildcard constraints are
a flexible system for specifying what a particular wildcard can, and cannot,
match using regular expressions.

```admonish info title="Regular expressions"

Regular expressions (commonly abbreviated "regexes" or "regexps") are a
mini-language for flexible string matching.

CTB: more here; give a few useful/common examples. \d+, alpha-numeric words, ??

Python comes with a friendly introduction to regexps that is a good
reference for more advanced use of regular expressions: see the
[Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html).
```

TODO:

* use in wildcards in rules
* use for glob_wildcards
* where else?
* named wildcards

## Using wildcard constraints in glob_wildcards

Let's start by looking at using wildcard constraints with
`glob_wildcards`.
Consider a directory containing the following files:
```
letters-only-abc-xyz.txt
letters-only-abc.txt
letters-only-abc2.txt
```
We could match all three files easily enough with:
```
files, = glob_wildcards('letters-only-{word}.txt')
```
which would give us `['abc2', 'abc-xyz', 'abc']`.

Now
suppose we only want our wildcard pattern to match `letters-only-abc.txt`,
but not the other files. How do we do this?

We can specify a constraint as below that only matches letters, not
numbers:
```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:letters-only}}
```
and the `letters_only` list will be `['abc']`

We can also specify characters to avoid, as opposed to characters that are
allowed, using the regexp `^` (NOT) character - this will match a broader
range of files than the previous example, but will still ignore words with
numbers in them:
```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:letters-only-2}}
```
Here, `letters_only` will be `['abc-xyz', 'abc']`, because we are allowing
anything _but_ numbers.

Avoiding certain characters is particularly useful when we want to
avoid matching in subdirectories.  By default, `glob_wildcards` will
include files in subdirectories - for example, if there is a file
`data/datafile.txt`, then `all_txt_files` below would list
`data/datafile.txt`:

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:all-txt}}
```

However, if we constrain the wildcard matching to avoid forward slashes (`/`)
then files in subdirectories will not be matched:

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:no-subdir}}
```

## Using wildcard constraints in rules

* only need in first place wildcard is mentioned

## Global wildcard constraints

snakemake supports _global_ wildcard constraints like so:

```python
wildcard_constraints:
    sample="\w+" # equivalent to {sample,\w+} - limits to alphabet letters
    num="[0-9]+" # equivalent to {num,[0-9]+} - limit to numbers
```

Anywhere where `sample` or `num` is used in the Snakefile, these
constraints will be applied.

<!-- CTB: check, can they be overridden locally? -->
