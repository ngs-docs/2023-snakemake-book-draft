# Installation and setup!

## Setup and installation

I suggest working in a new directory.

You'll need to [install snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) and [sourmash](https://sourmash.readthedocs.io/en/latest/#installing-sourmash). We suggest using [mamba, via miniforge/mambaforge](https://github.com/conda-forge/miniforge#mambaforge), for this.

### Getting the data:

You'll need to download these three files:

* [GCF_000021665.1_ASM2166v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/021/665/GCF_000021665.1_ASM2166v1/GCF_000021665.1_ASM2166v1_genomic.fna.gz)
* [GCF_000017325.1_ASM1732v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/017/325/GCF_000017325.1_ASM1732v1/GCF_000017325.1_ASM1732v1_genomic.fna.gz)
* [GCF_000020225.1_ASM2022v1_genomic.fna.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/020/225/GCF_000020225.1_ASM2022v1/GCF_000020225.1_ASM2022v1_genomic.fna.gz)

and rename them so that they are in a subdirectory `genomes/` with the names:
```
GCF_000017325.1.fna.gz
GCF_000020225.1.fna.gz
GCF_000021665.1.fna.gz
```

Note, you can download saved copies of them here, with the right names: [osf.io/2g4dm/](https://osf.io/2g4dm/).
