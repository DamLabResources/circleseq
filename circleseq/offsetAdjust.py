from __future__ import print_function
import glob
import argparse
import pandas as pd
import os
import re

def adjust(offset, read_size, folder):
    read_size-=1
    alloff= offset - read_size
    identified_folder = os.path.join(folder, 'identified', '*.txt')
    files = glob.glob(identified_folder)
    adjusted_folder = os.path.join(folder, 'adjusted')
    if not os.path.exists(adjusted_folder):
        os.makedirs(adjusted_folder)
    for f in files:
        name = f.split('/')[-1]
        outname = os.path.join(adjusted_folder, name)
        print(f)
        if re.search('.*coordinates.txt$', f):
            try:
                df = pd.read_csv(f, sep='\t', header=0)
                df.Read1_start_position = df.Read1_start_position + alloff
                df.Read2_start_position = df.Read2_start_position + alloff
                df.to_csv(outname, sep='\t', header=True, index=False)
            except ValueError:
                continue
        elif re.search('.*matched.txt', f):
            try:
                df = pd.read_csv(f, sep='\t', header=-1)
                df[1] = df[1] + alloff
                df[2] = df[2] + alloff -1
                df[8] = df[8] + alloff
                df[9] = df[9] + alloff
                df.to_csv(outname, sep='\t', header=False, index=False)
            except ValueError:
                continue

        elif re.search('.*count.txt', f):
            try:
                df = pd.read_csv(f, sep='\t', header=0)
                df.zero_based_Position = df.zero_based_Position + alloff
                df.to_csv(outname, sep='\t', header=True, index=False)
            except ValueError:
                continue
def main():
    parser = argparse.ArgumentParser(description="Adjust the coordinate on identified files\n"
                                                 "The coordinate will be off due to the read length and\n"
                                                 "the relative offset between PCR amplicon and HXB2\n"
                                                 "This script substitute the coordinate to index based\n"
                                                 "off of HXB2 reference sequence.")
    parser.add_argument('--offset', help='Distance from 1 position of HXB2', required =True, type=int)
    parser.add_argument('--read_size', help="Read length of expiremental fastq file [int]", required=True, type=int)
    parser.add_argument('--folder', help='Data folder for identified files from circleseq package', required=True)

    args = parser.parse_args()
    adjust(args.offset, args.read_size, args.folder)

if __name__ == '__main__':
    main()