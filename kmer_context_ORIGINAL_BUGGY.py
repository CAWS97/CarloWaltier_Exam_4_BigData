"""
Count k-mers and the letter that comes after each one in DNA sequences.

A k-mer is a short DNA substring of length k. This script also tracks the
letter that appears right after each k-mer in valid DNA lines.

Run with:
    python kmer_context_ORIGINAL_BUGGY.py

Input file should have one DNA sequence per line, using only A, C, G, and T.
Output file has one k-mer per line with its count and the counts of the letters
that come after it.
"""

import sys


def validate_sequence(sequence):
    """Check if a sequence only has A, C, G, and T.

    This is used so only valid DNA lines are counted when finding k-mers.

    Args:
        sequence (str): one DNA string to check.

    Returns:
        bool: True if the sequence is valid DNA, otherwise False.
    """
    valid = {"A", "C", "G", "T"}
    for char in sequence:
        if char not in valid:
            return False
    return True


def update_kmer_count(kmer_data, kmer, next_char):
    """Update the k-mer dictionary with one k-mer and its next letter.

    This keeps track of how many times each k-mer appears and what letter comes
    after it in the sequence.

    Args:
        kmer_data (dict): dictionary storing counts and next-letter data.
        kmer (str): the current k-mer substring.
        next_char (str): the character that follows the k-mer.

    Returns:
        None: updates kmer_data in place.
    """
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
    """Find every k-mer in a sequence and record the letter after it.

    This checks the sequence one position at a time to get each k-mer and the
    next character that follows it.

    Args:
        sequence (str): one DNA sequence.
        k (int): length of each k-mer.

    Returns:
        dict: a dictionary of k-mer counts and next-letter counts.
    """
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
    """Write the k-mer results to a file in sorted order.

    This saves each k-mer, its count, and the counts of letters that come after
    it, with the k-mers sorted A to Z.

    Args:
        kmer_data (dict): dictionary with k-mer and next-letter counts.
        output_file (str): file path where the results are written.

    Returns:
        None: writes the results to the given file.
    """
    with open(output_file, "w") as f:
        for kmer in sorted(kmer_data):  # Sort kmers lexicographically
            line = kmer + " " + str(kmer_data[kmer]["count"])
            for c in kmer_data[kmer]["next_chars"]:
                line += " " + c + ":" + str(kmer_data[kmer]["next_chars"][c])
            f.write(line + "\n")


def main():
    """Run the whole k-mer analysis with user prompts.

    This asks for the input file path, the k value, and the output path, then
    reads sequences, skips invalid DNA, counts k-mers, and saves the result.

    Args:
        None

    Returns:
        None: uses input prompts and writes the result file.
    """
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
            if not validate_sequence(sequence):
                # Confirm validator rejects only invalid DNA sequences
                print(f" Warning: Skipping invalid sequence: {sequence[:30]}")
                continue
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
