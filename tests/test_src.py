"""
Example pytest script:
you are looking for setup / teardown methods? py.test has fixtures:
    http://doc.pytest.org/en/latest/fixture.html
you find examples below
"""
import numpy as np
import pytest
from data_validation_module.src import (
    check_depth_string_zerofilled,
    check_range_from_zero_to_hundred,
    check_string_format_nnn_mmm,
    check_type_float,
    check_type_string,
)

BOTTOM_LIMIT = "999"


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
def test_check_type_float64_0(data, result):
    assert check_type_float(data) == result


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
    ],
)
def test_check_range_from_zero_to_hundred_0(data, result):
    assert check_range_from_zero_to_hundred(data) == result


@pytest.mark.parametrize(
    "top_limit, depth, result",
    [
        ("000", "030", True),
        ("000", "000", True),
        ("000", BOTTOM_LIMIT, True),
        ("001", "000", False),
        ("000", str(int(BOTTOM_LIMIT) + 1), False),
        ("000", "0030", False),
        ("000", "-123", False),
        ("000", "NA", False),
        ("000", 123, False),
        ("000", True, False),
        ("000", None, False),
        ("000", np.NaN, False),
        ("000", "NaN", False),
    ],
)
def test_check_depth_string_zerofilled_0(top_limit, depth, result):
    assert check_depth_string_zerofilled(top_limit, BOTTOM_LIMIT, depth) == result


@pytest.mark.parametrize(
    "data, result",
    [("SiCl", True), (34, False), (None, False), (np.NaN, False), (False, False)],
)
def test_check_type_string_0(data, result):
    assert check_type_string(data) == result


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
    ],
)
def test_check_string_format_nnn_mmm_0(data, result):
    assert check_string_format_nnn_mmm(data) == result
