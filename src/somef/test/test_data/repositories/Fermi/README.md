Getting Started
---------------

1. Acquire the fermi source code from the [download page][5] and compile with
   (`x.y` is the version number):

   		tar -jxf fermi-x.y.tar.bz2
   		(cd fermi-x.y; make)

2. Download the *C. elegans* reads [SRR065390][8] from SRA and convert to the
   FASTQ format with the `fastq-dump` tool from the [SRA toolkit][9]:

   		fastq-dump --split-spot SRR065390.lite.sra

3. Perform assembly with:

   		fermi-x.y/run-fermi.pl -ct8 -e fermi-x.y/fermi SRR065390.fastq > fmdef.mak
   		make -f fmdef.mak -j 8 > fmdef.log 2>&1

The entire procedure takes about several hours with 8 CPU cores. File
`fmdef.p5.fq.gz` contains the final contigs. The quality line in the FASTQ-like
format gives the per-base read depth computed from non-redundant
error-corrected reads.


FAQ
---

####0. In addition to this FAQ, are there any other documentations?

The algorithms and evaluations are described in the [fermi paper][11] with the
[preprint][1] available from arXiv. The detailed usage is documented in the
[fermi manpage][2].

####1. What is fermi?

Fermi is a de novo assembler for Illumina reads from whole-genome short-gun
sequencing. It also provides tools for error correction, sequence-to-read
alignment and comparison between read sets. It uses the FMD-index, a novel
compressed data structure, as the key data representation.

####2. How is fermi different from other assemblers?

For small genomes, fermi is not much different from other assemblers in terms
of performance. Nonetheless, for mammalian genomes, fermi is one of the few
choices that can do the job in a relatively small memory footprint. It can
assemble 35-fold human data in 90GB shared memory with an overall similar
contiguity and accuracy to other mainstream assemblers.

In addition to de novo assembly, fermi ultimately aims to preserve all the
information in the raw reads, in particular heterozygous events. SNP and INDEL
calling can be achieved by aligning the fermi unitigs to the reference genome
and has been shown to be advantageous over other approaches in some aspects (see
also the [preprint][1]).

####3. What is the relationship between fermi and SGA?

Fermi is substantially influenced by [SGA][3]. It follows a similar workflow,
including the idea of contrasting read sets.  On the other hand, the internal
implementation of fermi is distinct from that of SGA. Fermi is based on a novel
data structure and uses different algorithms for almost every step. As to the
end results, fermi has a similar performance to SGA for features shared between
them, and is arguably easier to use. In all, both fermi and SGA are viable
options for de novo assembly and contrast variant calling.

####4. Are there release notes?

Yes, below this FAQ.

####5. How to install fermi?

You may clone the [fermi github repository][4] to get the latest source code,
or acquire the source code of stable releases from the [download page][5]. You
can compile fermi by invoking `make` in the source code directory. The only
library dependency is [zlib][6]. After compilation, you may copy `fermi` and
`run-fermi.pl` to your `PATH` or simply use the executables in the source code
directory.

####6. How to run fermi for de novo assembly?

The [fermi manpage][2] shows an example. Briefly, if you have Illumina
short-insert paired-end reads `read1.fq.gz` and `read2.fq.gz`, you can run:

    run-fermi.pl -Pe ./fermi -t12 read1.fq.gz read2.fq.gz > fmdef.mak
    make -f fmdef.mak -j 12

to perform assembly using 12 CPU cores. The `fmdef.p5.fq.gz` gives the final
contigs using the paired-end information. If you only want to correct errors,
you may use

    make -f fmdef.mak -j 12 fmdef.ec.fq.gz

####7. What is contrast assembly? How can I use it?

The idea of contrast assembly was first proposed and has been implemented by
Jared Simpson and Richard Durbin. It works by assembling reads containing a
k-mer that is present in one set of reads but absent from another set of reads.
The contigs we get this way will span variants, including mutations and
breakpoints, only seen from the first set of reads. Mapping the contigs back
provides the locations. This approach directly focuses on the differences
between read sets and helps to reduce the complication of structural variations
and the imperfect reference genome.

To perform contrast assembly given two sets of reads, we need to generate
error-corrected FMD-index for both sets, use the `contrast` command to pick
reads unique to one read set, and then apply the `sub` command to extract
the FMD-index of selected reads. The following shows an example:

	# error correction for sample1; paired reads are interleaved in sample1.fq.gz
    run-fermi.pl -ct12 -p sample1 sample1.fq.gz > sample1.mak
	make -f sample1.mak -j 12 sample1.ec.rank
	# error correction for sample2
    run-fermi.pl -ct12 -p sample2 sample2.fq.gz > sample2.mak
	make -f sample2.mak -j 12 sample2.ec.rank
	# identify reads unique to one sample
	fermi contrast -t12 sample1.ec.fmd sample1.ec.rank sample1.sub sample2.ec.fmd sample2.ec.rank sample2.sub
	# generate the FMD-index for reads unique to sample1; similar applied to sample2
	fermi sub -t12 sample1.fmd sample1.sub > sample1.sub.fmd
	# assemble unique reads and perform graph simplification
	fermi unitig -l50 -t12 sample1.sub.fmd > sample1.sub.mag
	fermi clean -CA -l150 sample1.sub.mag > sample1-cleaned.sub.mag

We can align the resulting contigs `sample1-cleaned.sub.mag` to the reference
genome with [BWA-SW][10] to pinpoint the mutations and break points. It is also
possible to compare one sample to multiple samples by intersecting selected
reads using the `bitand` command and then performs the assembly.

A more convenient command-line interface is likely to be added in future.


[1]: http://arxiv.org/abs/1203.6364
[2]: https://github.com/lh3/fermi/blob/master/fermi.1
[3]: https://github.com/jts/sga
[4]: https://github.com/lh3/fermi
[5]: https://github.com/lh3/fermi/downloads
[6]: http://zlib.net/
[7]: https://github.com/lh3/fermi/blob/master/README.md
[8]: http://www.ncbi.nlm.nih.gov/sra?term=SRR065390
[9]: http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?cmd=show&f=software&m=software&s=software
[10]: https://github.com/lh3/bwa
[11]: http://bioinformatics.oxfordjournals.org/content/28/14/1838
[12]: http://www.springerlink.com/content/b55m96rj18462152/

Release Notes
-------------

###Release 1.1 (2012-08-22)

This release reduces the runtime of assembly by introducing an improved version
of the [BCR algorithm][12] for constructing FMD-index and by deploying
heuristics in error correction. On two human data sets, fermi takes 30% less
wall-clock time and produces slightly longer scaftigs, though at the cost of
marginally increased assembly break points in comparison to release 1.0.

(1.1: 2012-08-22, r744)

###Release 1.0 (2012-04-09)

This is the first public release of fermi, a de novo assembler and analysis
tool for whole-genome shot-gun sequencing. Source code can be acquired from
the [download page][5]. Please read the [manpage][2] and the [FAQ][7] for
detailed usage.

(1.0: 2012-04-09, r700)
