#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Credit: Alex Reynolds (Bioinformatics Stack Exchange)
Adapté pour une exécution modulaire ou directe
"""

import sys
import numpy as np

def process_record(header, sequence, low, high, output=sys.stdout):
    next_pos = 0
    last = 0
    fragment = 1
    while last < len(sequence) - high:
        next_pos = np.random.randint(low, high + 1) + last
        frag_seq = sequence[last:next_pos]
        output.write(f'{header}:{last}-{next_pos}:{fragment}\n{frag_seq}\n')
        last = next_pos
        fragment += 1

def parse_records(in_fn, low, high, output=sys.stdout):
    header = ""
    sequence = ""
    with open(in_fn, 'r') as ifh:
        for line in ifh:
            if line.startswith('>'):
                if sequence:
                    process_record(header, sequence, low, high, output)
                    sequence = ""
                header = line.strip()
            else:
                sequence += line.strip()
        if sequence:
            process_record(header, sequence, low, high, output)

def fragment_fasta(input_path, low, high):
    """
    Fonction appelable depuis un script Python.
    Retourne une fonction qui prend un fichier ouvert en écriture.
    """
    return lambda output: parse_records(input_path, low, high, output)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fragment_genomes.py <min_length> <max_length> <input_fasta>")
        sys.exit(1)

    low = int(sys.argv[1])
    high = int(sys.argv[2])
    input_file = sys.argv[3]

    parse_records(input_file, low, high)
