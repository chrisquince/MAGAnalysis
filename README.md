# MAGAnalysis
Collection of scripts for annotating and analysing genomes assembled from metagenomes

##Split clusters and find genes

This roughly summariese CQs standard approach to annotate metagenome assembled genomes (MAGs). Asker is going to have a go at rationalising this :)

First split the fasta file by cluster:

    ./SplitClusters.pl clustering_gt1000.csv Contigs_gt1000.fasta

Then call genes with prodigal (maybe better to use the original contig gene callings)?:

    ./Prodigal.sh

##Annotate to Kegg orthologs

First align each called gene against Kegg (Asker use Diamond and new Kegg database):

    ./RapsearchB.sh

Then map genes to KOs:
    ./AssignKO.sh

This calls the perl script:

Assign_KO.pl

The hardcoded path to Kegg gene->ortholog mapping in this perl script needs to be changed.

Then we collate all the *.hits files together:

    ./CollateHits.pl > CollateHits.csv

This will generate kegg ortholog frequencies for each cluster.

##Annotate to Kegg modules

Now we find which Kegg modules are present in each cluster by querying their [module reconstruct tool] (http://www.genome.jp/kegg/tool/map_module.html)

    python ./KO2MODULEclusters2.py -i CollateHits.csv -o Collate_modules.csv 


