# K-mer Context Analysis Tool

A Python script that counts k-mers in DNA sequences and the letter that comes right after each one.

## Overview

This tool reads DNA sequences and counts k-mers (short pieces of DNA of length k). For each k-mer, it also keeps track of which letter appeared right after it in the sequence. The results are written to a file, sorted from A to Z.

This kind of count is a starting point for genome assembly, where overlapping pieces of DNA are pieced back together to figure out the order of a whole genome.

## Features

- **DNA Validation**: Only sequences made of A, C, G, and T are used. Anything else is skipped with a warning.
- **K-mer Counting**: Counts every k-mer that has at least one letter following it.
- **Context Tracking**: Records which letter follows each k-mer and how many times.
- **Sorted Output**: K-mers in the output file are listed in alphabetical order.
- **Command-line Interface**: Runs in the terminal with three inputs.

## Repository Structure

```
.
├── README.md                         # This file
├── TEST_SUMMARY.md                   # Initial notes on bugs that were found and fixed early on
├── kmer_context_FINAL.py             # The main script
├── test_kmer_context.py              # Pytest test file
└── tests/
    ├── inputs/                       # Test input files
    │   ├── test_simple.txt
    │   ├── test_2_cross_sequence.txt
    │   ├── test_3_mixed_sequence.txt
    │   ├── test_4_edge_invalid.txt
    │   ├── test_5_mixedvalidity.txt
    │   └── test_6_comprehensive.txt
    └── expected_outputs/             # What the output should look like for each test
        ├── results_simple_sorted.txt
        ├── results_crossedmixed_sorted.txt
        ├── results_3_mixed_sequence_sorted.txt
        ├── results_4_edge_invalid.txt
        ├── results_5_mixedvalidity.txt
        └── results_6_comprehensive.txt
```

## Installation

### Prerequisites

- Python 3.6 or higher
- pytest (only needed if you want to run the tests)

### Setup

Clone the repository:

```bash
git clone https://github.com/CAWS97/CarloWaltier_Exam_4_BigData.git
cd CarloWaltier_Exam_4_BigData
```

Install pytest if you want to run the tests:

```bash
pip install pytest
```

## Usage

The script takes three things from the command line, in this order:

1. `input_file`: A file with DNA sequences, one per line.
2. `k`: The k-mer length (a number).
3. `output_file`: Where to save the results.

```bash
python kmer_context_FINAL.py <input_file> <k> <output_file>
```

### Example

```bash
python kmer_context_FINAL.py tests/inputs/test_simple.txt 2 results.txt
```

### Input Format

Input files should have one DNA sequence per line. Each sequence should only have A, C, G, and T (uppercase). Any line with other characters (numbers, lowercase letters, N, spaces, symbols, etc.) is skipped, and a warning is printed.

Example input:

```
ACGTACGT
TTTTAAAA
GCGCATGC
```

### Output Format

Each line in the output file has a k-mer, its total count, and the count of each letter that came after it. Only letters that actually showed up are listed. K-mers are in alphabetical order.

Example output (with k=2):

```
AA 2 A:1 T:1
AC 2 G:2
CG 1 T:1
GT 2 A:2
TA 1 C:1
...
```

## Testing

### Running Tests

From the top of the repo, run:

```bash
pytest -v
```

The `-v` flag tells pytest to list each test by name with its result.

### Test Coverage

The tests check:

- **Each function on its own**: `validate_sequence`, `update_kmer_count`, `count_kmers_with_context`, and `write_results_to_file`.
- **The whole script end to end**: running the full script on real input files and comparing the output to a saved expected file.
- **Edge cases**: invalid characters, sequences shorter than k, sequences exactly k long, repeated k-mers, and a really messy mixed-up sequence.

The test file is `test_kmer_context.py` and the test data is in `tests/inputs/` and `tests/expected_outputs/`.

## Functions

### `validate_sequence(sequence)`

Checks if a sequence only has A, C, G, and T.

- **`sequence`** *(str)*: the sequence to check.
- **Returns** *(bool)*: `True` if it's valid, `False` if not.

### `update_kmer_count(kmer_data, kmer, next_char)`

Updates the count for one k-mer and remembers the letter that came after it.

- **`kmer_data`** *(dict)*: dictionary that holds the k-mer counts and follower counts.
- **`kmer`** *(str)*: the k-mer to update.
- **`next_char`** *(str)*: the letter that came right after the k-mer.
- **Returns**: nothing — it just changes `kmer_data`.

### `count_kmers_with_context(sequence, k)`

Goes through one sequence and pulls out every k-mer along with the letter that follows it. The very last k-mer in a sequence has no follower, so it's not counted.

- **`sequence`** *(str)*: the DNA sequence to look at.
- **`k`** *(int)*: the k-mer length.
- **Returns** *(dict)*: a dictionary of each k-mer with its count and follower counts.

### `write_results_to_file(kmer_data, output_file)`

Writes all the k-mer results to a file, sorted A to Z.

- **`kmer_data`** *(dict)*: the k-mer data to save.
- **`output_file`** *(str)*: where to save the file.
- **Returns**: nothing — it writes to the file.

### `main()`

Reads the command-line inputs, goes through the input file one sequence at a time, adds up the counts across every valid sequence, and writes the final results to the output file.

## Bugs Fixed in the Original Script

The original script had a few bugs that this version fixes:

1. **Counts didn't add up across sequences.** The old code reset `kmer_data` for each sequence and called `write_results_to_file` inside the loop with `'w'` mode, so the output file only had the last sequence's results. Fixed by setting up `all_kmer_data` outside the loop and writing the combined result once at the end.
2. **Output wasn't really sorted.** The old code did call `sorted()`, but because the file was being overwritten for each sequence, the final file wasn't sorted across all the data. The aggregation fix took care of this too.
3. **The validator was too loose.** The original `validate_sequence` only rejected numbers, so lowercase letters, N, spaces, and symbols all got through. Tightened so every character has to be A, C, G, or T.
4. **Skipped sequences were silent.** Added a warning message when an invalid line is skipped, so the user can see why a line was dropped.

## AI Use Statement

- Using Visual Studio Code Debugger, and assistant to push and commit changes.
- Claude (Anthropic's AI) for drafting this README, and generating a final test_kmer_context with all of the tests I had accrued beforehand in the test file.
- Help writing the function that sorts k-mers alphabetically (lexicographically) in the output file. better readme version and push/commit! 
