#!/bin/bash

for file in */*faa
do
	dir=${file%.faa}
	echo $file
	echo $dir

	if [ ! -f ${dir}B.m8 ]; then
		rapsearch -q $file -d /srv/chris/Databases/keggs_database/KeggUpdate/genes/fasta/kegg_genes -o ${dir}B -z 64 	
	fi
done
