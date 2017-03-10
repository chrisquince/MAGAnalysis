from Bio import SeqIO

import argparse
import sys
import os
from collections import defaultdict

def main(argv):
    parser = argparse.ArgumentParser()
                
    parser.add_argument('fasta_file', help=("sequences"))
    
    parser.add_argument('cluster_file', help=("clusters"))

    args = parser.parse_args()

    fasta_dict = {}
    handle = open(args.fasta_file, "rU")
    
    for record in SeqIO.parse(handle, "fasta"):
        seq = record.seq
        fasta_dict[record.id] = str(seq)

    handle.close()

    clusters = defaultdict(list)
    with open(args.cluster_file) as f:
        for i,line in enumerate(f):
            line = line.rstrip()
            tokens = line.split(",")
            clusters[tokens[1]].append(tokens[0])


    for clust, seqs in clusters.iteritems():
        if not os.path.exists(clust):
            os.makedirs(clust)

        for seq in seqs:
            f = open(str(clust) + "/" + seq + ".fa" ,"w")
            
            f.write(">" + seq + "\n")

            f.write(fasta_dict[seq] + "\n")

            f.close()

if __name__ == "__main__":

    main(sys.argv[1:])

