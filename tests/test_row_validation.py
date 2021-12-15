import datetime as datetime
from pathlib import Path, PosixPath
from typing import Union

import numpy as np
import pandas as pd
import pytest

from data_validation_module.row_validations import (
    check_int_greater_zero,
    check_positive_int,
    check_positive_int_or_Null,
    check_string_available_for_database,
    check_type_of_row,
    datestring_has_format_yyyy_mm_dd,
    is_a_dictionary,
    is_a_list_with_unique_lowercase_db_strings,
    is_a_list_with_unique_lowercase_strings,
    is_a_lowercase_db_string,
    is_greater_zero_or_null,
    is_neither_npnan_nor_none,
    is_string_represent_json,
    is_type_string,
    is_type_timestamp,
    is_valid_dir_path,
    is_valid_file_path,
    is_valid_latitude,
    is_valid_longitude,
    is_valid_percent_value_or_null,
    is_valid_ratio_value_or_null,
    is_valid_schema_and_table,
    string_has_format_nnn_mmm,
)

NUMERIC = Union[float, int]


@pytest.mark.parametrize(
    "row_item, result",
    [(np.NaN, False), (1, True), (True, True), ("aaa", True), (None, False)],
)
def test_check_none_and_nan(row_item, result: bool):
    assert is_neither_npnan_nor_none(row_item) == result


@pytest.mark.parametrize(
    "row_item, row_item_type, result",
    [
        (23.456, "float", True),
        (int(45), "int", True),
        ("aaa", "str", True),
        (None, "NoneType", True),
        (False, "bool", True),
        (pd.Timestamp("2016-03-03 00:00:00"), "Timestamp", True),
        (np.NaN, "float", True),
    ],
)
def test_check_all_types(row_item, row_item_type: str, result: bool):
    assert check_type_of_row(row_item, row_item_type) == result


@pytest.mark.parametrize(
    "row_item, result",
    [
        (float(23.456), True),
        (23.456, True),
        (45, False),
        ("a45", False),
        (None, False),
        (int(23.456), False),
        (float(23), True),
        (np.NaN, True),
    ],
)
def test_check_type_of_row_float(row_item: float, result: bool):
    assert check_type_of_row(row_item, "float") == result


@pytest.mark.parametrize(
    "percent, result",
    [
        (23.45, True),
        (0.0, True),
        (100.0, True),
        (102.2, False),
        (-12.34, False),
        ("23", False),
        (34, True),
        (True, False),
        (None, True),
        ("alp_num", False),
        (np.NaN, True),
    ],
)
def test_is_valid_percent_value_or_null(percent: NUMERIC, result: bool):
    assert is_valid_percent_value_or_null(percent) == result


@pytest.mark.parametrize(
    "ratio, result",
    [
        (0.45, True),
        (0.0, True),
        (1.23, False),
        (-0.34, False),
        ("0.23", False),
        (True, False),
        (None, True),
        ("alp_num", False),
        (np.NaN, True),
    ],
)
def test_is_valid_ratio_value_or_null(ratio: NUMERIC, result: bool):
    assert is_valid_ratio_value_or_null(ratio) == result


@pytest.mark.parametrize(
    "data, result",
    [("SiCl", True), (34, False), (None, False), (np.NaN, False), (False, False)],
)
def test_check_type_of_row_string(data: str, result: bool):
    assert is_type_string(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("005_030", True),
        ("05_030", False),
        ("005", False),
        ("030_1000", False),
        ("string", False),
        ("NA_030", False),
        ("005_NA", False),
        ("NA_NA", False),
        (34, False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("0050030", False),
        ("alp_num", False),
        ("030_005", False),
    ],
)
def test_string_has_format_nnn_mmm(data: str, result: bool):
    assert string_has_format_nnn_mmm(data) == result


@pytest.mark.parametrize(
    "date, result",
    [
        ("1998-08-18", True),
        ("2200-01-01", False),
        ("1800-01-01", False),
        ("2001-18-01", False),
        ("2001-01-32", False),
        (1482, False),
        ("1482", False),
        ("a45", False),
        ("NaT", False),
        (None, False),
        (np.int64(23), False),
        (np.float64(23), False),
        (np.NaN, False),
    ],
)
def test_datestring_has_format_yyyy_mm_dd(date: str, result: bool):
    assert datestring_has_format_yyyy_mm_dd(date) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (45, True),
        (23.456, False),
        (float(45), False),
        ("a45", False),
        (None, False),
        (23.456, False),
        (float(23), False),
        (np.NaN, False),
    ],
)
def test_check_type_of_row_int(data: int, result: bool):
    assert check_type_of_row(data, "int") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (pd.Timestamp("2016-03-03 00:00:00"), True),
        (datetime.datetime(2016, 3, 3, 0, 0), False),
        ("2016-03-03", False),
        (None, False),
        (False, False),
        (np.NaN, False),
        (10, False),
    ],
)
def test_check_type_of_row_timestamp(data: pd.Timestamp, result: bool):
    assert is_type_timestamp(data) == result


@pytest.mark.parametrize(
    "latitude, result",
    [
        (45.1, True),
        (-45.1, True),
        (45, True),
        (91.1, False),
        (-91.1, False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("alp_num", False),
    ],
)
def test_is_valid_latitude(latitude: NUMERIC, result: bool):
    assert is_valid_latitude(latitude) == result


@pytest.mark.parametrize(
    "longitude, result",
    [
        (123.4, True),
        (-123.4, True),
        (45, True),
        (191.1, False),
        (-191.1, False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("alp_num", False),
    ],
)
def test_is_valid_longitude(longitude: NUMERIC, result: bool):
    assert is_valid_longitude(longitude) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (-23, False),
        (1, True),
        (0, True),
        (23.456, False),
        (45.0, True),
        ("a45", False),
        (None, False),
        (int(23.456), True),
        (float(23.34), False),
        (np.NaN, False),
    ],
)
def test_check_positive_int(data: int, result: bool):
    assert check_positive_int(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (-23, False),
        (1, True),
        (0, False),
        (23.456, False),
        (45.0, True),
        ("a45", False),
        (None, False),
        (int(23.456), True),
        (float(23.34), False),
        (np.NaN, False),
    ],
)
def test_check_positive_int_from_0(data: int, result: bool):
    assert check_int_greater_zero(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (-23, False),
        (1, True),
        (45, True),
        (23.456, False),
        ("a45", False),
        (None, True),
        (int(23.456), True),
        (float(23), True),
        (np.NaN, True),
    ],
)
def test_check_positive_int_or_Null(data: int, result: bool):
    assert check_positive_int_or_Null(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (float(23.456), True),
        (0.0, False),
        (0.1, True),
        (-23.456, False),
        (45, True),
        ("a45", False),
        (None, True),
        (int(23.456), True),
        (float(23), True),
        (np.NaN, True),
    ],
)
def test_is_positive_not_zero_number_or_null(data: NUMERIC, result: bool):
    assert is_greater_zero_or_null(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("a1pha_numeric", True),
        ("{", False),
        ("[", False),
        ("(", False),
        ("&", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_check_string_available_for_database(data: str, result: bool):
    assert check_string_available_for_database(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (Path("../data_validation_module/test_files"), True),
        (PosixPath("../data_validation_module/test_files"), True),
        (PosixPath("test_files/dictionary_config.json"), False),
        (PosixPath("/foo/foo.bar"), False),
        (Path("/foo/foo.bar"), False),
        (PosixPath("foo/foo"), False),
        ("/foo/foo", False),
        ("foo", False),
        (None, False),
        (np.NaN, False),
    ],
)
def test_is_valid_dir_path(data: Path, result: bool):
    assert is_valid_dir_path(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (Path("src/data_validation_module"), False),
        (PosixPath("test_files/test_json.json"), True),
        (Path("test_files/test_json.json"), True),
        (PosixPath("/foo/foo.bar"), False),
        (Path("/foo/foo.bar"), False),
        (PosixPath("foo/foo"), False),
        ("/foo/foo", False),
        ("foo", False),
        (None, False),
        (np.NaN, False),
    ],
)
def test_is_valid_file_path(data: Path, result: bool):
    assert is_valid_file_path(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("foo/foo.json", True),
        ("foo.json/", False),
        ("foo++.json", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_string_represent_json(data: str, result: bool):
    assert is_string_represent_json(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ({"a": 1}, True),
        ("{'a': 1}", False),
        ([1, 2, 3], False),
        ({"a", "b", "c"}, False),
        ("&", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_a_dictionary(data: dict, result: bool):
    assert is_a_dictionary(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (["a%", "b ", "c_"], True),
        (["a%", 1, "c_"], False),
        ([], False),
        (["a", "a", "c"], False),
        (["a%", "bbB", "c_"], False),
        (["a%", "B", "c_"], False),
        ({"a", "b", "c"}, False),
        ("string", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_a_list_with_unique_lowercase_strings(data: list, result: bool):
    assert is_a_list_with_unique_lowercase_strings(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (["a", "b", "c"], True),
        ([], False),
        (["a", "bb[", "c"], False),
        (["a", "bbB", "c"], False),
        (["a", "a", "c"], False),
        ({"a", "b", "c"}, False),
        ("string", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_a_list_with_unique_strings(data: str, result: bool):
    assert is_a_list_with_unique_lowercase_db_strings(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("string_._string", True),
        ("a1pha_numeric", False),
        ("string.string.string", False),
        ("string.STRING", False),
        ("char%^{.string", False),
        ("]", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_valid_schema_and_table(data: str, result: bool):
    assert is_valid_schema_and_table(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("a1pha_numeric", True),
        ("A1PHA_NUMERIC", False),
        ("a1pha.numeric", False),
        ("{", False),
        ("[", False),
        ("(", False),
        ("&", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_is_a_lowercase_db_string(data: str, result: bool):
    assert is_a_lowercase_db_string(data) == result
