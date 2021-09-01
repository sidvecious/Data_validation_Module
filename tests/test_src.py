"""
Example pytest script:
you are looking for setup / teardown methods? py.test has fixtures:
    http://doc.pytest.org/en/latest/fixture.html
you find examples below
"""
import datetime as datetime
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import requests
from data_validation_module.src import (
    check_dataframe,
    check_date_format_or_NaT,
    check_date_format_YYYY_mm_dd,
    check_depth_string_zerofilled,
    check_double_90_180,
    check_positive_int,
    check_positive_int_or_Null,
    check_range_0_100,
    check_range_from_zero_to_hundred,
    check_string_available_for_database,
    check_string_format_nnn_mmm,
    check_string_format_nnn_mmm_with_NA,
    check_type_of_row,
    get_df_name,
    iterate_column,
    iterate_data_config,
    read_json_file,
    split_invalid_data_rows,
)
from file_path_tools.search_and_find import find_closest_filepath
from pandas._testing import assert_frame_equal

BOTTOM_LIMIT = "999"
DATAFRAME_DICT = {
    "date_id": check_date_format_YYYY_mm_dd,
    "depth_id": check_string_format_nnn_mmm,
    "soil_texture": check_type_of_row,
}

SERIES_DICT = {
    "date_id": check_date_format_or_NaT,
    "depth_id": check_string_format_nnn_mmm_with_NA,
}

"""

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
def test_check_type_of_row_float64_0(data, result):
    assert check_type_of_row(data, np.float64) == result


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
        ("000", "NA", True),
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
def test_check_type_of_row_string_0(data, result):
    assert check_type_of_row(data, str) == result


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
def test_check_type_of_row_int64_0(data, result):
    assert check_type_of_row(data, np.int64) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (pd.Timestamp('2016-03-03 00:00:00'), True),
        (datetime.datetime(2016, 3, 3, 0, 0), False),
        ("2016-03-03", False),
        (None, False),
        (False, False),
        (np.NaN, False),
        (10, False)

    ],
)
def test_check_type_of_row_timestamp_0(data, result):
    assert check_type_of_row(data, pd.Timestamp) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("005_030", True),
        ("05_030", False),
        ("005", False),
        ("030_1000", False),
        ("string", False),
        ("NA_030", True),
        ("005_NA", True),
        ("NA_NA", True),
        (34, False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("0050030", False),
        ("alp_num", False),
        ("030_005", False),
    ],
)
def test_check_string_format_nnn_mmm_with_NA_0(data, result):
    assert check_string_format_nnn_mmm_with_NA(data) == result


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
        ("NaT", True),
        (None, False),
        (np.int64(23), False),
        (np.float64(23), False),
        (np.NaN, False),
    ],
)
def test_check_date_format_or_NaT_0(data, result):
    assert check_date_format_or_NaT(data) == result


@pytest.mark.parametrize(
    "coordinate, axis, result",
    [
        (np.float64(45.1), 'lat', True),
        (np.float64(-45.1), 'lat', True),
        (np.int64(45), 'lat', False),
        (np.float64(91.1), 'lat', False),
        (np.float64(-91.1), 'lat', False),
        (np.float64(123.4), 'lon', True),
        (np.float64(-123.4), 'lon', True),
        (np.int64(45), 'lon', False),
        (np.float64(191.1), 'lon', False),
        (np.float64(-191.1), 'lon', False),
        (None,'lat', False),
        (None,'lon', False),
        (np.NaN, 'lat', False),
        (np.NaN, 'lon', False),
        (False, 'lat', False),
        (False, 'lon', False),
        ("alp_num", 'lat', False),
        ("alp_num", 'lon', False),
    ],
)
def test_check_double_90_180_0(coordinate, axis, result):
    assert check_double_90_180(coordinate, axis) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.float64(90.12), True),
        (np.float64(-90.12), False),
        (np.float64(110.12), False),
        (np.float64(100.0), True),
        (np.float64(0.0), True),
        (np.int64(90), False),
        (34, False),
        (None, False),
        (np.NaN, False),
        (False, False),
        ("90.12", False),
        ("alp_num", False),
    ],
)
def test_check_range_0_100_0(data, result):
    assert check_range_0_100(data) == result


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
def test_check_positive_int_0(data, result):
    assert check_positive_int(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        (np.int64(-23), False),
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
def test_check_positive_int_or_Null_0(data, result):
    assert check_positive_int_or_Null(data) == result


@pytest.mark.parametrize(
    "data, result",
    [
        ("a1pha_numeric", True),
        ("{}", False),
        ("[]", False),
        ("()", False),
        ("&", False),
        (None, False),
        (23, False),
        (np.NaN, False),
    ],
)
def test_check_string_available_for_database_0(data, result):
    assert check_string_available_for_database(data) == result


#@pytest.mark.parametrize(
#    "top_limit, depth, result",
#    [
#        ("000", "030", True),
#        ("000", "000", False),
#        ("000", BOTTOM_LIMIT, True),
#        ("001", "000", False),
#        ("000", str(int(BOTTOM_LIMIT) + 1), False),
#        ("000", "0030", False),
#        ("000", "-123", False),
#        ("000", "NA", True),
#        ("000", 123, False),
#        ("000", True, False),
#        ("000", None, False),
#        ("000", np.NaN, False),
#        ("000", "NaN", False),
#    ],
#)
#def test_check_depth_zerofilled_or_NA_0(top_limit, depth, result):
#    assert check_depth_zerofilled_or_NA(top_limit, BOTTOM_LIMIT, depth) == result


def test_check_dataset_depth_id_col_0(test_depth_id_column, test_invalid_list_depth_id):
    assert (
        iterate_column(test_depth_id_column, 'depth_id') == test_invalid_list_depth_id
    )


def test_check_date_id_col_0(test_date_id_column, test_invalid_list_date_id):
    assert (
        iterate_column(test_date_id_column, 'date_id') == test_invalid_list_date_id
    )


def test_check_soil_texture_col_0(test_soil_texture_column, test_invalid_list_date_id):
    assert (
        iterate_column(test_soil_texture_column, "soil_texture") == test_invalid_list_date_id
    )
"""


def test_read_json_file(test_data_config, test_string_dataframe_config_json):
    data_conf = read_json_file(test_string_dataframe_config_json)
    assert data_conf == test_data_config


def test_get_df_name(test_df, test_df_name):
    name = get_df_name(test_df)
    assert name == test_df_name


def test_iterate_data_config(
    test_df_name, test_data_config, test_df, test_invalid_list
):
    list = iterate_data_config(test_df_name, test_data_config, test_df)
    assert all(a == b for a, b in zip(list, test_invalid_list))


def test_split_invalid_data_row_0(test_invalid_df, test_df_with_invalid_column_filled):
    # 1. remove invalid_rows.csv
    dir = find_closest_filepath("data_validation_module/test_files")
    try:
        os.remove(dir / "invalid_rows.csv")
    except IOError:
        pass

    # 2. assert invalid_rows.csv
    split_invalid_data_rows(test_df_with_invalid_column_filled)
    df = pd.read_csv(dir / "invalid_rows.csv")
    assert df.shape == test_invalid_df.shape

    # 3. remove invalid_rows.csv
    os.remove(dir / "invalid_rows.csv")


def test_split_invalid_data_row_1(test_valid_df, test_df_with_invalid_column_filled):
    df = split_invalid_data_rows(test_df_with_invalid_column_filled)
    assert df.shape == test_valid_df.shape


def test_check_dataframe(test_df, test_valid_df, test_string_dataframe_config_json):
    df = check_dataframe(test_df, test_string_dataframe_config_json)
    assert df.shape == test_valid_df.shape
