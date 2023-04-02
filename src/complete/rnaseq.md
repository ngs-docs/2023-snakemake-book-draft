# A complete RNAseq example

Below, we provide a simple yet complete RNAseq analysis workflow.
From start to finish, this workflow takes in four yeast RNAseq
read data sets and then:

* generates FastQC reports for each data set;
* runs Trimmomatic to remove low quality RNAseq reads;
* runs FastQC on the trimmed reads;
* uses salmon to quantify the coding sequences represented in each of the
  read data sets;
* uses DESeq2 to load, normalize, and contrast gene expression in the
  conditions represented by the samples.
  
The distinguish new feature of this workflow over the variant calling and
assembly worklows is that a significant amount of the processing is done
in R, in an RMarkdown file.
  
CTB: do we want to split out the FastQC/multiqc stuff into its own example?
  
TODO:

* acknowledge authors!
* do we write this as a collection of chapters or as a single chapter?
* build workflow diagram

## Exercies

add new data sets
add some examples of pulling out specific genes by name

