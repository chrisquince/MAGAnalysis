#!/bin/bash
while read line
do
    cog=$line
    echo $cog
     ./SelectCogsSCG.pl ../clustering_gt1000_scg.tsv ../../Annotate/Contigs_gt1000_c10K.fas $cog > SCGs/$cog.ffn
done < cogs.txt

