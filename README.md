# MAGAnalysis
Collection of scripts for annotating and analysing genomes assembled from metagenomes

##Split clusters and find genes

This roughly summariese CQs standard approach to annotate metagenome assembled genomes (MAGs). Asker is going to have a go at rationalising this :)

First split the fasta file by cluster:

    ./SplitClusters.pl Contigs_gt1000.fasta clustering_gt1000.csv 

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

##Split Cogs

Somewhat unsatisfactorilly we do use the COG annotations across all contigs and split those across clusters. It would be better to develop a coherent strategy for this:

    ./SplitCOGs.pl Contigs_gt1000.cogs clustering_gt1000.csv

Where we have annotated cogs on the contigs using:

    python ./ExtractCogsNative.py -b Contigs_gt1000.rpsout --cdd_cog_file $PATH_TO_CONCOCT/CONCOCT/scgs/cdd_to_cog.tsv > Contigs_gt1000.cogs

where Contigs_gt1000.rpsout is the RPS blast output against the COG database  

##Construct a phylogenetic tree

Assume we are starting from the 'Split' directory in which we have seperated out the cluster fasta files and we have done the COG assignments for each cluster. Then the first step is to extract each of the 36 conserved core COGs individually. There is an example bash script GetSCG.sh for doing this in phyloscripts but it will need modifying:

```
#!/bin/bash
while read line
do
    cog=$line
    echo $cog
     ./SelectCogsSCG.pl ../clustering_gt1000_scg.tsv ../../Annotate/Contigs_gt1000_c10K.fna $cog > SCGs/$cog.ffn
done < cogs.txt
``` 

Run this after making a directory SCGs and it will create one file for each SCG with the corresponding nucleotide sequences from each cluster but only for this with completeness (> 0.75) hard coded in the perl script somewhere you should check that :)

Then we align each of these cog files against my prepared database containing 1 genome from each bacterial genera and archael species:
```
#!/bin/bash

mkdir AlignAll

while read line
do
    cog=$line
    echo $cog
    cat /gpfs/chrisq/chris/Databases/NCBI/Combined/Cogs/All_$cog.ffn SCGs/${cog}.ffn > AlignAll/${cog}_all.ffn
    mafft --thread 64 AlignAll/${cog}_all.ffn > AlignAll/${cog}_all.gffn
done < cogs.txt
```

