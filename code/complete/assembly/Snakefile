wildcard_constraints:
    lines="\d+"

rule all:
    input:
        'SRR2584857.full.contigs.fa', 'SRR2584857.100000.contigs.fa',
        'SRR2584857.full.annot', 'SRR2584857.100000.annot',
        'SRR2584857.full.quast', 'SRR2584857.100000.quast',

rule assemble:
    input:
        r1="{sample}_1.fastq.gz",
        r2="{sample}_2.fastq.gz",
    output: directory("{sample}.full.out")
    shell: """
        megahit -1 {input.r1} -2 {input.r2} -f -m 20e9 -t 16 -o {output}
    """

rule subsample:
    input:
        r1="{sample}_1.fastq.gz",
        r2="{sample}_2.fastq.gz",
    output:
        r1="{sample}_1.{lines}.fastq.gz",
        r2="{sample}_2.{lines}.fastq.gz",
    shell: """
        gunzip -c {input.r1} | \
		head -{wildcards.lines} | \
		gzip > {output.r1} \
		|| true
        gunzip -c {input.r2} | \
		head -{wildcards.lines} | \
		gzip > {output.r2} \
		|| true
    """

rule assemble_subset:
    input:
        r1="{sample}_1.{lines}.fastq.gz",
        r2="{sample}_2.{lines}.fastq.gz",
    output: directory("{sample}.{lines}.out")
    shell: """
        megahit -1 {input.r1} -2 {input.r2} -f -m 5e9 -t 4 -o {output}
    """

# copy the final.contigs.{something}.fa file out of the megahit assembly directory
rule copy_genome_contigs2:
    input:
        "{sample}.{label}.out"
    output:
        "{sample}.{label}.contigs.fa"
    shell:
        "cp {input}/final.contigs.fa {output}"

# annotate an assembly using prokka; *.contigs.fa -> *.prokka
rule annotate_contigs:
    input:
        "{prefix}.contigs.fa"
    output:
        directory("{prefix}.annot")
    threads: 8
    conda: "env-prokka.yml"
    shell:
        # note: a bug in prokka+megahit means we have to force success.
        # that's what "|| :" does.
        "prokka --outdir {output} --prefix {wildcards.prefix} {input} --cpus {threads} || :"

# evaluate an assembly using quast; *.contigs.fa => *.quast
rule quast_eval:
    input:
        "{prefix}.contigs.fa"
    conda: "env-quast.yml"      # note, you need to run this with --use-conda!
    output:
        directory("{prefix}.quast")
    shell: "quast {input} -o {output}"
