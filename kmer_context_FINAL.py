"""
Count k-mers and the letter that comes after each one in DNA sequences.

A k-mer is a short DNA substring of length k. This script also tracks the
letter that appears right after each k-mer in valid DNA lines.

Run with:
    python kmer_context_FINAL.py <input_file> <k> <output_file>

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
    """Run the whole k-mer analysis from the command line.

    This reads the input file, k value, and output path from command-line
    arguments, then reads sequences, skips invalid DNA, counts k-mers, and
    saves the result to the output file.

    Args:
        None

    Returns:
        None: reads from command-line arguments and writes the result file.
    """
    # Check that the user provided the right number of arguments
    if len(sys.argv) != 4:
        print("Usage: python kmer_context_FINAL.py <input_file> <k> <output_file>")
        sys.exit(1)

    # Read arguments from the command line
    input_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]

    # Build up k-mer data across every valid sequence in the file
    all_kmer_data = {}
    with open(input_file) as f:
        for line in f:
            sequence = line.strip()
            if not validate_sequence(sequence):
                # Skip and warn about any line that isn't valid DNA
                print(f" Warning: Skipping invalid sequence: {sequence[:30]}")
                continue
            kmer_data = count_kmers_with_context(sequence, k)
            # Merge this sequence's counts into the running total
            for kmer, data in kmer_data.items():
                if kmer not in all_kmer_data:
                    all_kmer_data[kmer] = {"count": 0, "next_chars": {}}
                all_kmer_data[kmer]["count"] += data["count"]
                for next_char, count in data["next_chars"].items():
                    if next_char in all_kmer_data[kmer]["next_chars"]:
                        all_kmer_data[kmer]["next_chars"][next_char] += count
                    else:
                        all_kmer_data[kmer]["next_chars"][next_char] = count

    # Write the combined results, sorted alphabetically
    write_results_to_file(all_kmer_data, output_file)


if __name__ == "__main__":
    main()
