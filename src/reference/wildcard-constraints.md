
CTB: in progress

Link to snakemake official documentation on wildcard constraints: 
https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#constraining-wildcards

Link to Python "friendly" regexp documentation: https://docs.python.org/3/howto/regex.html

You can use wildcard constraints with all wildcards to avoid matching too much.

* use in wildcards in rules
* use for glob_wildcards
* where else?

## Using wildcard constraints in glob_wildcards

Suppose you have two files, `letters-only-abc.txt` and `letters-only-abc2.txt`,
and you only want to match the first pattern with `glob_wildcards`. You can
specify a constraint as below that only matches letters, not numbers:

```python
{{#include ../../code/misc/wildcards/wildcards.snakefile:letters-only}}
```

You can also specify characters to avoid, as opposed to characters that are
allowed, using the regexp `^` (NOT) character -

XXX

This is particularly useful when you want to avoid matching in subdirectories.
By default, `glob_wildcards` will include files in subdirectories - for
example, if there is a file `data/datafile.txt`, then `all_txt_files` below
would list `data/datafile.txt`:

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
