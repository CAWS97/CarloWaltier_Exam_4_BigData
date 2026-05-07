"""
test_kmer_context.py
--------------------
This file holds all the pytest tests for kmer_context_FINAL.py.

To run all the tests, type this in the terminal:
    pytest -v

The tests are split into groups. Each group checks one function. At the
bottom there are end-to-end tests that run the whole script on real input
files and check the output matches what we expect.
"""

import os
import subprocess
import sys

import pytest

from kmer_context_FINAL import (
    validate_sequence,
    update_kmer_count,
    count_kmers_with_context,
    write_results_to_file,
)


# Folder where this test file lives. Used to find the script and test files.
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(TEST_DIR, "tests", "inputs")
EXPECTED_DIR = os.path.join(TEST_DIR, "tests", "expected_outputs")


# ---------------------------------------------------------------------------
# Tests for validate_sequence
# ---------------------------------------------------------------------------

def test_validate_sequence_accepts_valid_dna():
    """A short DNA sequence with only A, C, G, T should be valid."""
    assert validate_sequence("ATCG") is True

def test_validate_sequence_accepts_long_valid_dna():
    """A longer DNA sequence with only A, C, G, T should still be valid."""
    assert validate_sequence("ATCGATCGATCG") is True

def test_validate_sequence_rejects_digits():
    """A sequence with numbers in it should not be valid."""
    assert validate_sequence("ATCG123") is False

def test_validate_sequence_rejects_lowercase():
    """A sequence with lowercase letters should not be valid."""
    assert validate_sequence("atcg") is False

def test_validate_sequence_rejects_n():
    """The letter N is not one of A, C, G, T, so it should not be valid."""
    assert validate_sequence("ATCGN") is False

def test_validate_sequence_rejects_special_characters():
    """A sequence with symbols like ! should not be valid."""
    assert validate_sequence("ATCG!") is False

def test_validate_sequence_rejects_spaces():
    """A sequence with a space in it should not be valid."""
    assert validate_sequence("ATCG ATCG") is False

def test_validate_sequence_empty_string():
    """An empty sequence has nothing bad in it, so it counts as valid."""
    assert validate_sequence("") is True

def test_validate_sequence_rejects_gnarly_mixed_garbage():
    """A long messy sequence with all kinds of bad stuff should not be valid."""
    gnarly = "CATCATCATCATGCATGCATGCGCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA78AAAAAAAAAAAgcatgcatgcatgcatCGACGAABCDEFGHIJCATGHSDKJGHTCAGCTAC123/.,-=-`/.,GCTATTTGCCTAGC"
    assert validate_sequence(gnarly) is False


# ---------------------------------------------------------------------------
# Tests for update_kmer_count
# ---------------------------------------------------------------------------

def test_update_kmer_count_adds_new_kmer():
    """Adding a new k-mer for the first time should give it a count of 1."""
    kmer_data = {}
    update_kmer_count(kmer_data, "AT", "C")
    assert kmer_data["AT"]["count"] == 1
    assert kmer_data["AT"]["next_chars"] == {"C": 1}

def test_update_kmer_count_increments_existing_kmer():
    """Adding the same k-mer twice should make the count go up to 2."""
    kmer_data = {}
    update_kmer_count(kmer_data, "AT", "C")
    update_kmer_count(kmer_data, "AT", "C")
    assert kmer_data["AT"]["count"] == 2
    assert kmer_data["AT"]["next_chars"] == {"C": 2}

def test_update_kmer_count_tracks_multiple_followers():
    """A k-mer can have different letters after it, and they should all be counted."""
    kmer_data = {}
    update_kmer_count(kmer_data, "AT", "C")
    update_kmer_count(kmer_data, "AT", "G")
    update_kmer_count(kmer_data, "AT", "C")
    assert kmer_data["AT"]["count"] == 3
    assert kmer_data["AT"]["next_chars"] == {"C": 2, "G": 1}

def test_update_kmer_count_handles_multiple_kmers():
    """Different k-mers should each get their own spot in the dictionary."""
    kmer_data = {}
    update_kmer_count(kmer_data, "AT", "C")
    update_kmer_count(kmer_data, "TC", "G")
    assert kmer_data["AT"]["count"] == 1
    assert kmer_data["TC"]["count"] == 1


# ---------------------------------------------------------------------------
# Tests for count_kmers_with_context
# ---------------------------------------------------------------------------

def test_count_kmers_simple_sequence():
    """The sequence ATCG with k=2 should give AT followed by C and TC followed by G."""
    result = count_kmers_with_context("ATCG", 2)
    assert result["AT"]["count"] == 1
    assert result["AT"]["next_chars"] == {"C": 1}
    assert result["TC"]["count"] == 1
    assert result["TC"]["next_chars"] == {"G": 1}

def test_count_kmers_skips_final_kmer_without_follower():
    """The very last k-mer in a sequence has no letter after it, so we skip it."""
    result = count_kmers_with_context("ATCG", 2)
    # CG is at the end of ATCG with nothing after it, so it should not be in the result
    assert "CG" not in result

def test_count_kmers_repeated_kmer():
    """The sequence AAAA with k=2 gives AA twice, both followed by A."""
    result = count_kmers_with_context("AAAA", 2)
    assert result["AA"]["count"] == 2
    assert result["AA"]["next_chars"] == {"A": 2}

def test_count_kmers_with_k3():
    """Make sure the function actually uses the k value we pass in."""
    result = count_kmers_with_context("ATCGAT", 3)
    assert result["ATC"]["count"] == 1
    assert result["ATC"]["next_chars"] == {"G": 1}
    assert result["TCG"]["count"] == 1
    assert result["TCG"]["next_chars"] == {"A": 1}

def test_count_kmers_sequence_too_short():
    """If the sequence is shorter than k, we get an empty dictionary back."""
    result = count_kmers_with_context("A", 2)
    assert result == {}

def test_count_kmers_sequence_equals_k():
    """A sequence the same length as k has no follower, so the result is empty."""
    result = count_kmers_with_context("AT", 2)
    assert result == {}


# ---------------------------------------------------------------------------
# Tests for write_results_to_file
# ---------------------------------------------------------------------------

def test_write_results_creates_file(tmp_path):
    """The function should actually make a file when we tell it to write."""
    kmer_data = {"AT": {"count": 1, "next_chars": {"C": 1}}}
    output_file = tmp_path / "out.txt"
    write_results_to_file(kmer_data, str(output_file))
    assert output_file.exists()

def test_write_results_correct_format(tmp_path):
    """Each line should look like 'kmer count letter:count'."""
    kmer_data = {"AT": {"count": 3, "next_chars": {"C": 2, "G": 1}}}
    output_file = tmp_path / "out.txt"
    write_results_to_file(kmer_data, str(output_file))
    contents = output_file.read_text().strip()
    # The line should start with the k-mer and its total count
    assert contents.startswith("AT 3")
    # Both followers should show up somewhere on the line
    assert "C:2" in contents
    assert "G:1" in contents

def test_write_results_sorted_alphabetically(tmp_path):
    """The k-mers in the file should be sorted from A to Z."""
    kmer_data = {
        "TT": {"count": 1, "next_chars": {"A": 1}},
        "AA": {"count": 1, "next_chars": {"T": 1}},
        "GG": {"count": 1, "next_chars": {"C": 1}},
    }
    output_file = tmp_path / "out.txt"
    write_results_to_file(kmer_data, str(output_file))
    lines = output_file.read_text().strip().split("\n")
    # Grab the first letter of each line and check they are in order
    first_chars = [line[0] for line in lines]
    assert first_chars == sorted(first_chars)


# ---------------------------------------------------------------------------
# End-to-end tests: run the whole script on real input files
# ---------------------------------------------------------------------------

def run_script(input_file, k, output_file):
    """Helper that runs kmer_context_FINAL.py from the command line for us."""
    script_path = os.path.join(TEST_DIR, "kmer_context_FINAL.py")
    result = subprocess.run(
        [sys.executable, script_path, input_file, str(k), output_file],
        capture_output=True,
        text=True,
    )
    return result

def read_lines_sorted(path):
    """Read a file, drop blank lines, and return the lines sorted A to Z.

    We sort the lines because the order of letters after a k-mer might come
    out a little different in different Python versions, but we still want
    the test to count it as a match.
    """
    with open(path) as f:
        return sorted(line.strip() for line in f if line.strip())

def test_end_to_end_simple(tmp_path):
    """Running the script on test_simple.txt should match the expected file."""
    input_file = os.path.join(INPUTS_DIR, "test_simple.txt")
    expected_file = os.path.join(EXPECTED_DIR, "results_simple_sorted.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    assert read_lines_sorted(str(output_file)) == read_lines_sorted(expected_file)

def test_end_to_end_cross_sequence(tmp_path):
    """This test catches the bug where counts were not combined across sequences.

    The k-mer AA shows up in both sequences, so the counts from each one
    have to be added together to get the right total.
    """
    input_file = os.path.join(INPUTS_DIR, "test_2_cross_sequence.txt")
    expected_file = os.path.join(EXPECTED_DIR, "results_crossedmixed_sorted.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    assert read_lines_sorted(str(output_file)) == read_lines_sorted(expected_file)

def test_end_to_end_mixed_sequence(tmp_path):
    """Running the script on test_3_mixed_sequence.txt should match the expected file."""
    input_file = os.path.join(INPUTS_DIR, "test_3_mixed_sequence.txt")
    expected_file = os.path.join(EXPECTED_DIR, "results_3_mixed_sequence_sorted.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    assert read_lines_sorted(str(output_file)) == read_lines_sorted(expected_file)

def test_end_to_end_invalid_input(tmp_path):
    """Every sequence in test_4_edge_invalid.txt is bad, so the output should be empty."""
    input_file = os.path.join(INPUTS_DIR, "test_4_edge_invalid.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    # Nothing should make it into the output file because every line is invalid
    assert output_file.read_text().strip() == ""

def test_end_to_end_mixed_validity(tmp_path):
    """Some sequences are valid and some are not, and the output should match the expected file."""
    input_file = os.path.join(INPUTS_DIR, "test_5_mixedvalidity.txt")
    expected_file = os.path.join(EXPECTED_DIR, "results_5_mixedvalidity.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    assert read_lines_sorted(str(output_file)) == read_lines_sorted(expected_file)

def test_end_to_end_comprehensive(tmp_path):
    """A bigger mixed test with lots of valid and invalid sequences."""
    input_file = os.path.join(INPUTS_DIR, "test_6_comprehensive.txt")
    expected_file = os.path.join(EXPECTED_DIR, "results_6_comprehensive.txt")
    output_file = tmp_path / "out.txt"
    run_script(input_file, 2, str(output_file))
    assert read_lines_sorted(str(output_file)) == read_lines_sorted(expected_file)

def test_script_handles_missing_args():
    """If you run the script without giving it the right inputs, it should print Usage and stop."""
    script_path = os.path.join(TEST_DIR, "kmer_context_FINAL.py")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
    )
    # The script should not finish normally (return code should not be 0)
    assert result.returncode != 0
    # The word "Usage" should show up in the printed message
    assert "Usage" in result.stdout or "Usage" in result.stderr