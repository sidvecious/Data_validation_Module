import datetime as datetime

import numpy as np
import pandas as pd
import pytest
from data_validation_module.data_validation_module.row_validations import (
    check_date_format_YYYY_mm_dd,
    check_double_90,
    check_double_180,
    check_none,
    check_positive_int,
    check_positive_int_or_Null,
    check_range_from_zero_to_hundred,
    check_string_available_for_database,
    check_string_format_nnn_mmm,
    check_type_of_row,
)


@pytest.mark.parametrize(
    "data, result",
    [(np.NaN, False), (1, True), (True, True)],
)
def test_check_none_0(data, result: bool):
    assert check_none(data, float) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.float64(23.456), True),
        (23.456, False),
        (45, False),
        ("a45", False),
        (None, False),
        (np.int64(23.456), False),
        (np.float64(23), True),
        (np.NaN, False),
    ],
)
def test_check_all_0(data, result: bool):
    assert check_type_of_row(data, "float64") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.float64(23.456), True),
        (23.456, False),
        (45, False),
        ("a45", False),
        (None, False),
        (np.int64(23.456), False),
        (np.float64(23), True),
        (np.NaN, False),
    ],
)
def test_check_type_of_row_float64_0(data, result: bool):
    assert check_type_of_row(data, "float64") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.float64(23.45), True),
        (np.float64(0.0), True),
        (np.float64(100.0), True),
        (np.float64(102.2), False),
        (np.float64(-12.34), False),
        ("23", False),
        (np.int64(34), False),
        (True, False),
        (None, False),
        (np.NaN, False),
        ("alp_num", False),
    ],
)
def test_check_range_from_zero_to_hundred_0(data, result: bool):
    assert check_range_from_zero_to_hundred(data, "float64") == result


@pytest.mark.parametrize(
    "data, result",
    [("SiCl", True), (34, False), (None, False), (np.NaN, False), (False, False)],
)
def test_check_type_of_row_string_0(data, result: bool):
    assert check_type_of_row(data, "str") == result


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
def test_check_string_format_nnn_mmm_0(data, result: bool):
    assert check_string_format_nnn_mmm(data, "str") == result


@pytest.mark.parametrize(
    "data, result",
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
def test_check_date_format_YYYY_mm_dd_0(data, result: bool):
    assert check_date_format_YYYY_mm_dd(data, "str") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.int64(45), True),
        (23.456, False),
        (45, False),
        ("a45", False),
        (None, False),
        (np.int64(23.456), True),
        (np.float64(23), False),
        (np.NaN, False),
    ],
)
def test_check_type_of_row_int64_0(data, result: bool):
    assert check_type_of_row(data, "int64") == result


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
def test_check_type_of_row_timestamp_0(data, result: bool):
    assert check_type_of_row(data, "Timestamp") == result


@pytest.mark.parametrize(
    "coordinate, result",
    [
        (np.float64(45.1), True),
        (np.float64(-45.1), True),
        (np.int64(45), False),
        (np.float64(91.1), False),
        (np.float64(-91.1), False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("alp_num", False),
    ],
)
def test_check_double_90(coordinate, result: bool):
    assert check_double_90(coordinate, "float64") == result


@pytest.mark.parametrize(
    "coordinate, result",
    [
        (np.float64(123.4), True),
        (np.float64(-123.4), True),
        (np.int64(45), False),
        (np.float64(191.1), False),
        (np.float64(-191.1), False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("alp_num", False),
    ],
)
def test_check_double_180(coordinate, result: bool):
    assert check_double_180(coordinate, "float64") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.int64(-23), False),
        (np.int64(1), True),
        (np.int64(0), False),
        (23.456, False),
        (45, False),
        ("a45", False),
        (None, False),
        (np.int64(23.456), True),
        (np.float64(23), False),
        (np.NaN, False),
    ],
)
def test_check_positive_int_0(data, result: bool):
    assert check_positive_int(data, "int64") == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.int64(-23), False),
        (0, False),
        (np.int64(45), True),
        (23.456, False),
        (45, False),
        ("a45", False),
        (None, True),
        (np.int64(23.456), True),
        (np.float64(23), False),
        (np.NaN, False),
    ],
)
def test_check_positive_int_or_Null_0(data, result: bool):
    assert check_positive_int_or_Null(data, "int64") == result


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
def test_check_string_available_for_database_0(data, result: bool):
    assert check_string_available_for_database(data, "str") == result
