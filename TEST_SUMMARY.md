# Initial Test Summary

## Updated Files
- `kmer_context_ORIGINAL_BUGGY.py`
- `test_simple.txt`
- `results_simple.txt`

## Initial Bugs Fixed

### Off-by-one counting error in `update_kmer_count()`:
- **First Problem:** Count initialized to 1, then incremented, making all counts 1 too high
- **Fix:** Initialize count to 0 instead

### `IndexError` in kmer extraction in `count_kmers_with_context()`:
- **Second Problem:** Loop range `range(len(sequence) - k + 1)` caused `i+k` to exceed sequence length
- **Fix:** Changed to `range(len(sequence) - k)` to ensure valid indices

### Command-line argument errors in `main()`:
- **Third Problem:** Used `sys.argv[1]`, `sys.argv[2]`, `sys.argv[3]` causing `IndexError` when no args provided
- **Fix:** Replaced with interactive `input()` prompts

### Output file handling in `main()`:
- **Fourth Problem:** `write_results_to_file()` keeping only last sequence's results
- **Fix:** Accumulate all kmer data first, then write once

## Result
The script now analyzes k-mers across all sequences in the input file and produces a result output file.

## Test Run
Tested with `test_simple.txt` using `k = 2` and output written to `results_simple.txt`.
