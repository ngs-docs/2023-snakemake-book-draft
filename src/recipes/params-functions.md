# Subsetting FASTQ files to a fixed number of records.

In [the subsampling files recipe](./subsampling-files.md), we
showed how to output a file with a specific number of lines in it
based only on the output filename. What if we want to sample a
specific number of _records_ from a FASTQ file? To do this we
need to transform the number of records in a wildcard into the number
of lines.

To do this, snakemake supports functions in its `params:` blocks (ref
CTB XXX params blocks). In the following recipe, we calculate the
number of lines to sample based on the number of _records_ specified
in the `num_records` wildcard:

```python
{{#include ../../code/examples/params.subset/Snakefile}}
```

There are two special components here:

* the Python function `calc_num_lines` takes a wildcards object as a
  parameter, and calculates the number of lines to subset based on the
  value of `wildcards.num_records`;
* then, the `params:` block applies `calc_num_lines` to generate
  `params.num_lines`, which can then be used in the shell command.
  
  
References:
* CTB params
* CTB namespaces
* CTB python code

## Using lambda

The recipe above is pretty long - you can make a much shorter (but
also harder to understand!) Snakefile using using anonymous "lambda"
functions:

```python
{{#include ../../code/examples/params.subset_lambda/Snakefile}}
```

Here, `lambda` creates an anonymous function that takes a single parameter,
`wildcards`, and returns the value of `wildcards.num_records` multipled by
4.
