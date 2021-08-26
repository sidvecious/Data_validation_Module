"""
Example pytest script:
you are looking for setup / teardown methods? py.test has fixtures:
    http://doc.pytest.org/en/latest/fixture.html
you find examples below
"""
import numpy as np
import pandas as pd
import pytest
from data_validation_module.src import (
    check_dataset_date_id_col,
    check_dataset_depth_id_col,
    check_date_format_YYYY_mm_dd,
    check_depth_string_zerofilled,
    check_range_from_zero_to_hundred,
    check_sample_gdf,
    check_string_format_nnn_mmm,
    check_type_float,
    check_type_string,
    split_invalid_data_rows,
)
from file_path_tools.search_and_find import find_closest_filepath
from pandas._testing import assert_frame_equal

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
        ("030_005", False),
    ],
)
def test_check_string_format_nnn_mmm_0(data, result):
    assert check_string_format_nnn_mmm(data) == result


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
def test_check_date_format_YYYY_mm_dd_0(data, result):
    assert check_date_format_YYYY_mm_dd(data) == result


def test_check_dataset_depth_id_col(test_depth_id_column, test_invalid_list_depth_id):
    empty_list = []
    assert (
        check_dataset_depth_id_col(empty_list, test_depth_id_column)
        == test_invalid_list_depth_id
    )


def test_check_date_id_col(test_date_id_col, test_invalid_list_date_id):
    empty_list = []
    assert (
        check_dataset_date_id_col(empty_list, test_date_id_col)
        == test_invalid_list_date_id
    )


def test_check_sample_gdf(test_df, test_df_control):
    df_test = check_sample_gdf(test_df)
    assert_frame_equal(test_df_control, df_test)


def test_split_invalid_data_rows_1(test_df_control):
    test_data_dir = find_closest_filepath("soil_data_harmonization/test_files")
    split_invalid_data_rows(test_df_control, test_data_dir)
    invalid_rows_df = pd.read_csv(test_data_dir / "test_invalid_rows.csv")
    assert invalid_rows_df.count == 2
