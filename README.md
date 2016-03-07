# MAGAnalysis
Collection of scripts for annotating and analysing genomes assembled from metagenomes

This roughly summariese CQs standard approach to annotate metagenome assembled genomes (MAGs). Asker is going to have a go at rationalising this :)

First split the fasta file by cluster:

    ./SplitClusters.pl clustering_gt1000.csv Contigs_gt1000.fasta

Then call genes with prodigal (maybe better to use the original contig gene callings)?:

    ./Prodigal.sh


