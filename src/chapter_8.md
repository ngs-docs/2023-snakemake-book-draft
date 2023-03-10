# Chapter 8 - adding new genomes

So we've got a new genome, and we can build a sketch for it. Let's
add it into our comparison, so we're building comparison matrix
for _four_ genomes, and not just three!

To add this new genome in to the comparison, all you need to do is add
the sketch into the `compare_genomes` input, and snakemake will
automatically locate the associated genome file and run
`sketch_genome` on it (as in the previous chapter), and then run
`compare_genomes` on it.  snakemake will take care of the rest!

```python
{{#include ../code/section2/interm4.snakefile}}
```

Now when you run `snakemake -j 3 plot_comparison` you will get a
`compare.mat.matrix.png` file that contains a 4x4 matrix! (See Figure.)

![4x4 matrix comparison of genomes](images/2023-snakemake-slithering-section-2-4x4-mat.png)

Note that the workflow diagram has now expanded to include our fourth genome, too!

![interm3 graph of jobs](images/2023-snakemake-slithering-section-2-interm4-dag.png?raw=true)

