#!/bin/bash

mkdir AlignAll

while read line
do
    cog=$line
    echo $cog
    cat /gpfs/chrisq/chris/Databases/NCBI/Combined/Cogs/All_$cog.ffn SCGs/${cog}.ffn > AlignAll/${cog}_all.ffn
    mafft --thread 64 AlignAll/${cog}_all.ffn > AlignAll/${cog}_all.gffn
done < cogs.txt
