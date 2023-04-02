rule download_data:
    output: "SRR2584857_1.fastq.gz"
    shell: """
        curl -JLO https://osf.io/4rdza/download -o {output}
    """

rule download_genome:
    output: "ecoli-rel606.fa.gz"
    shell:
        "curl -JLO https://osf.io/8sm92/download -o {output}"

rule map_reads:
    input:
        reads="SRR2584857_1.fastq.gz",
        ref="ecoli-rel606.fa.gz"
    output: "SRR2584857_1.x.ecoli-rel606.sam"
    shell: """
        minimap2 -ax sr {input.ref} {input.reads} > {output}
    """

rule sam_to_bam:
    input: "SRR2584857_1.x.ecoli-rel606.sam",
    output: "SRR2584857_1.x.ecoli-rel606.bam",
    shell: """
        samtools view -b -F 4 {input} > {output}
     """

rule sort_bam:
    input: "SRR2584857_1.x.ecoli-rel606.bam"
    output: "SRR2584857_1.x.ecoli-rel606.bam.sorted"
    shell: """
        samtools sort {input} > {output}
    """

rule call_variants:
    input:
        ref="ecoli-rel606.fa.gz",
        bam="SRR2584857_1.x.ecoli-rel606.bam.sorted",
    output:
        pileup="SRR2584857_1.x.ecoli-rel606.pileup",
        ref="ecoli-rel606.fa",
        bcf="SRR2584857_1.x.ecoli-rel606.bcf",
        vcf="SRR2584857_1.x.ecoli-rel606.vcf",
    shell: """
        gunzip -k {input.ref}
        bcftools mpileup -Ou -f {output.ref} {input.bam} > {output.pileup}
        bcftools call -mv -Ob {output.pileup} -o {output.bcf}
        bcftools view {output.bcf} > {output.vcf}
    """
