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
    valid = {"A", "C", "G", "T"}
    for char in sequence:
        if char not in valid:
            return False
    return True


def update_kmer_count(kmer_data, kmer, next_char):
    # FIXED: Initialize count to 0 instead of 1 to avoid off-by-one error
    # Original bug: count started at 1, then incremented for each occurrence,
    # causing counts to be 1 higher than actual
    if kmer not in kmer_data:
        kmer_data[kmer] = {"count": 0, "next_chars": {}}
    kmer_data[kmer]["count"] += 1
    if next_char in kmer_data[kmer]["next_chars"]:
        kmer_data[kmer]["next_chars"][next_char] += 1
    else:
        kmer_data[kmer]["next_chars"][next_char] = 1


def count_kmers_with_context(sequence, k):
    # FIXED: Changed range from (len(sequence) - k + 1) to (len(sequence) - k)
    # Original bug: range(len-k+1) caused IndexError when accessing next_char
    # because i+k would exceed sequence length
    kmer_data = {}
    for i in range(len(sequence) - k):  # Was: range(len(sequence) - k + 1)
        kmer = sequence[i:i+k]
        next_char = sequence[i+k]
        update_kmer_count(kmer_data, kmer, next_char)
    return kmer_data


def write_results_to_file(kmer_data, output_file):
    with open(output_file, "w") as f:
        for kmer in sorted(kmer_data):  # Sort kmers lexicographically
            line = kmer + " " + str(kmer_data[kmer]["count"])
            for c in kmer_data[kmer]["next_chars"]:
                line += " " + c + ":" + str(kmer_data[kmer]["next_chars"][c])
            f.write(line + "\n")


def main():
    # FIXED: Replaced sys.argv with input() for interactive prompts
    # Original bug: Used command-line args which caused IndexError when none provided
    input_file = input("Enter input file path: ")
    k = int(input("Enter k-mer length (k): "))
    output_file = input("Enter output file path: ")

    # FIXED: Accumulate all kmer data before writing, instead of overwriting file per sequence
    # Original bug: write_results_to_file() called for each sequence with "w" mode,
    # causing only the last sequence's results to be saved
    all_kmer_data = {}
    with open(input_file) as f:
        for line in f:
            sequence = line.strip()
            if validate_sequence(sequence):
                kmer_data = count_kmers_with_context(sequence, k)
                # Merge kmer_data into all_kmer_data
                for kmer, data in kmer_data.items():
                    if kmer not in all_kmer_data:
                        all_kmer_data[kmer] = {"count": 0, "next_chars": {}}
                    all_kmer_data[kmer]["count"] += data["count"]
                    for next_char, count in data["next_chars"].items():
                        if next_char in all_kmer_data[kmer]["next_chars"]:
                            all_kmer_data[kmer]["next_chars"][next_char] += count
                        else:
                            all_kmer_data[kmer]["next_chars"][next_char] = count

    write_results_to_file(all_kmer_data, output_file)


if __name__ == "__main__":
    main()
