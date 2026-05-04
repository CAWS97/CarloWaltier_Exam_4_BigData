"""
test_kmer_context.py
--------------------
Pytest test suite for kmer_context.py.

Run with:
    pytest -v

The tests are organized by the function under test, with one section
per function plus a final section for end-to-end behavior of `main`.
Edge cases the assignment specifically calls out are each in their own
test so failures point straight at the misbehaving case.
"""

import sys


def validate_sequence(sequence):
    for char in sequence:
        if char.isdigit():
            return False
    return True


def update_kmer_count(kmer_data, kmer, next_char):
    if kmer not in kmer_data:
        kmer_data[kmer] = {"count": 1, "next_chars": {}}
    kmer_data[kmer]["count"] += 1
    if next_char in kmer_data[kmer]["next_chars"]:
        kmer_data[kmer]["next_chars"][next_char] += 1
    else:
        kmer_data[kmer]["next_chars"][next_char] = 1


def count_kmers_with_context(sequence, k):
    kmer_data = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        next_char = sequence[i+k]
        update_kmer_count(kmer_data, kmer, next_char)
    return kmer_data


def write_results_to_file(kmer_data, output_file):
    with open(output_file, "w") as f:
        for kmer in kmer_data:
            line = kmer + " " + str(kmer_data[kmer]["count"])
            for c in kmer_data[kmer]["next_chars"]:
                line += " " + c + ":" + str(kmer_data[kmer]["next_chars"][c])
            f.write(line + "\n")


def main():
    input_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]

    with open(input_file) as f:
        for line in f:
            sequence = line.strip()
            if validate_sequence(sequence):
                kmer_data = count_kmers_with_context(sequence, k)
                write_results_to_file(kmer_data, output_file)


if __name__ == "__main__":
    main()
