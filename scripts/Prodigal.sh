#!/bin/bash

for file in Cluster*/Cluster*fa
do
    stub=${file%.fa}

    if [ ! -f ${stub}_prodigal.faa ]; then 
    	prodigal -p meta -i $file -a ${stub}_prodigal.faa -d ${stub}_prodigal.fas > $stub.out
    fi

    echo $file
done
