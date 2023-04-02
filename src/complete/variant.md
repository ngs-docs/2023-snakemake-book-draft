# A complete variant calling example for a bacterial genome

Here, we provide a simple introductory variant calling workflow
for a bacterial genome. It assumes a haploid genome and it produces
both unfiltered and quality-filtered variant calls. The workflow
takes a single-ended read data set from the E. coli LTEE, and then:

* uses minimap2 to align the reads to a reference genome and produce a SAM file;
* converts the SAM file to a BAM file;
* sorts and indexes the BAM file;
* uses mpileup to generate a set of variant calls in a binary format;
* converts the binary format into a text VCF file;
* filters the calls based on coverage and quality.
