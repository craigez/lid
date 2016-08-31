from . import prep

import os
import pytest


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

def test_span_tokenize():
    result = prep._span_tokenize("a bc\nde f")
    expected = [(0,1), (2,4), (5,7), (8,9)]
    assert result == expected

    result = prep._span_tokenize(["a bc", "de f"])
    assert result == expected

def test_tokens_and_positions_by_line():
    tok, pos = prep._tokens_and_positions_by_line(["a bc", "de f"])
    assert tok == [["a", "bc"], ["de", "f"]]
    assert pos == [[(0,1), (2,4)], [(0,2), (3,4)]]

def test_prep_license():
    path = os.path.join(BASE_DIR, "data", "test", "license", "test_license.txt")
    lic = prep.License.from_filename(path)
    assert len(lic.lines) == 1

    lic = prep.License.from_lines(["  ab c,d.  ", "\t", "   ef   "])
    assert list(lic.get_ignored_strings()) == ["  ", " ", "", "", "", "  \n\t\n   ", "   \n"]

def test_prep_source():
    path = os.path.join(BASE_DIR, "data", "test", "data", "test1.py")
    src = prep.Source.from_filename(path)
    assert src.lines == ["zero", "one two three four", "five", "six", "seven"]

    src_subset_1 = src.subset(0, 2)
    assert src_subset_1.lines == ["zero", "one two three four"]
    assert src_subset_1.original_line_offset == 0

    src_subset_2 = src.subset(3, 5)
    assert src_subset_2.lines == ["six", "seven"]
    assert src_subset_2.original_line_offset == 3

    src_subset_3 = src_subset_2.subset(1, 2)
    assert src_subset_3.lines == ["seven"]
    assert src_subset_3.original_line_offset == 4

def test_source_tokens_by_line():
    src = prep.Source.from_lines(["  ab  cd  ", "", "   ef   "])
    assert src.tokens_by_line == [["ab", "cd"], [], ["ef"]]
    assert src.token_positions_by_line == [[(2,4), (6,8)], [], [(3,5)]]

def test_source_get_ignored_strings():
    src = prep.Source.from_lines([])
    assert src.tokens_by_line == []
    assert list(src.get_ignored_strings()) == [""]

    src = prep.Source.from_lines(["   ", "  ", " "])
    assert src.tokens_by_line == [[], [], []]
    assert list(src.get_ignored_strings()) == ["   \n  \n \n"]

    src = prep.Source.from_lines(["  ab c,d.  ", "\t", "   ef   "])
    assert src.tokens_by_line == [["ab", "c", ",", "d", "."], [], ["ef"]]
    expected = ["  ", " ", "", "", "", "  \n\t\n   ", "   \n"]
    assert list(src.get_ignored_strings()) == expected

def test_license_library():
    license_dir = os.path.join(BASE_DIR, "data", "test", "license")
    license_library = prep.LicenseLibrary.from_path(license_dir)
    assert set(["test_license", "custom_license"]) == set(license_library.licenses.keys())
