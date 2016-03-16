#!/usr/bin/env python

import sqlite3 as sq
import os
from collections import defaultdict
import argparse

def main():
    parser = argparse.ArgumentParser(description="Extract contigs belonging to bins directly from concoct or from Anvi'o profile")
    parser.add_argument('-f','--fasta', help='Path to fasta file of contigs', required=True)
    parser.add_argument('-o','--output', help='Path to output directory', required=True)
    parser.add_argument('-a','--anvio', help='Path to anvio profile', required=False)
    parser.add_argument('-c','--concoct', help='Path to CONCOCT clustering result', required=False)
    parser.add_argument('-p','--proteins', help='Prodigal proteins file', required=False)
    args = parser.parse_args()
    if args.concoct is None and args.anvio is None:
        raise Exception("Must give either -a or -c")
    if args.anvio is None:
        contigstoextract = get_cluster_contigs(args.concoct)
    if args.concoct is None:
        contigstoextract = get_anvio_contigs(args.anvio)
    print len(contigstoextract)
    outputdir = args.output
    contigsfile = args.fasta
    contigsdict = small_fasta_parser(contigsfile)

    if args.proteins is not None:
        proteinsdict = small_fasta_parser(args.proteins)
        proteinscontigsdict = defaultdict(list)
        for key, value in proteinsdict.iteritems():
            if key == '':
                continue
            proteinscontigsdict["_".join(key.split("_")[0:-1])].append(value)
    
    os.mkdir(outputdir)
    for binname, contigs in contigstoextract.iteritems():
        os.mkdir(outputdir + '/' + binname)
        temp_output = open(outputdir + '/' + binname + '/bincontigs.fa', 'w')
        temp_output_proteins = open(outputdir + '/' + binname + '/binproteins.faa', 'w')
        for contig in contigs:
            print >>temp_output, '>' + contig
            print >>temp_output, contigsdict[contig]
            for prot in proteinscontigsdict[contig]:
                print >>temp_output_proteins, ">" + contig
                print >>temp_output_proteins, prot
            
    temp_output.close()
    temp_output_proteins.close()

def small_fasta_parser(fasta_file):
    seqs = defaultdict(list)
    current_seq_name = ""
    current_seq = ""
    for line in open(fasta_file, 'r'):
        if line[0] == '>':
            seqs[current_seq_name] = current_seq
            current_seq_name = line.replace(">", "").strip().split(" ")[0]
            current_seq = ""
        else:
            current_seq += line.strip()
    return seqs
            
def get_cluster_contigs(clustering_file):
    contigs = defaultdict(list)
    for line in open(clustering_file):
        contig = line.strip().split(",")[0]
        cluster = line.strip().split(",")[1]
        contigs[cluster].append(contig)
    return contigs

def get_anvio_contigs(anvioprofile):
    anvicon = sq.connect(anvioprofile)
    anvicur = anvicon.cursor()
    anvicur.execute("select group_concat(split), cluster_id from collections_of_splits group by cluster_id")
    contigs = {x[1]: x[0].replace("_split_00001", "").split(",") for x in anvicur.fetchall()} #check the replace
    anvicon.close()
    return contigs

if __name__ == '__main__':
    main()


