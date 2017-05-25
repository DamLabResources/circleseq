from __future__ import print_function
from Bio import SeqIO
import argparse
from subprocess import check_call
import shlex

def readRef(extra_ref_path, ref_path, read_size, exout, finalout):
    names = []
    read_size-=1
    with open(exout, 'w') as handle:
        for seq in SeqIO.parse(extra_ref_path, 'fasta'):
            seq.seq = seq.seq[-read_size:] + seq.seq + seq.seq[:read_size]
            names.append(seq.id)
            SeqIO.write(seq, handle, 'fasta')
    cmd = 'cat %s %s' % (exout, ref_path)
    with open(finalout, 'w') as handle:
        check_call(shlex.split(cmd), stdout=handle)

    return names

def main():
    parser = argparse.ArgumentParser(description="Reconstruct reference genome.\n"
                                                 "Construct partially redundant sequence for extra chromosomes\n"
                                                 "and append original reference genome to it."
                                     , formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-e", "--extra", help="Extra reference sequence filename", required=True)
    parser.add_argument("-r", "--reference", help="Original reference genome filename", required=True)
    parser.add_argument("-s", "--read_size", help="Read length of expiremental fastq file [int]", required=True, default=75, type=int)
    parser.add_argument("--exout", help="Output filename of extra chromosomes", required=True)
    parser.add_argument("--out", help="Final output reference filename", required=True)
    args = parser.parse_args()
    readRef(args.extra, args.reference, args.read_size, args.exout, args.out)


if __name__ == "__main__":
    main()
