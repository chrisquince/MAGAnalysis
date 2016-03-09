#!/bin/bash
while read line
do
    cog=$line
    echo $cog
     ./SelectCogsSCG.pl ../clustering_gt2000_scg.tsv ../../Annotate_gt2k/Contigs_gt2000_c10K.fas $cog > SCGs/$cog.ffn
done < cogs.txt
