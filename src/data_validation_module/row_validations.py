"""
file with the row validation functions
"""

import re
from datetime import datetime
from typing import Tuple, Union

import numpy as np
import pandas as pd
from loguru import logger

NUMERIC = Union[float, int]


# the basic function for every type check accept bool, none, nan, str, int, float and Timestamp
# It should accept also any other class
def check_type_of_row(row_item, row_item_type: str) -> bool:
    try:
        return type(row_item).__name__ == row_item_type
    except Exception as err:
        logger.error(f"something goes wrong with {row_item}, {row_item_type}, {err}")
        return False


# for: gdf in upload_to_postgresql if has valid Timestamp
def is_type_timestamp(date_stamp: pd.Timestamp) -> bool:
    return check_type_of_row(date_stamp, "Timestamp")


# for: gdf in upload_to_postgresql if has valid string
def is_type_string(string: str) -> bool:
    return check_type_of_row(string, "str")


# is called only when the expected type is an instance of numpy for exclude np.NaN
def is_neither_npnan_nor_none(row_item: float) -> bool:
    if check_type_of_row(row_item, "float") and np.isnan(row_item):
        return False
    elif row_item is None:
        return False
    return True


# for: upload_ready_data, in the target columns with 'percent'
def is_valid_percent_value_or_null(percent: NUMERIC) -> bool:
    if is_numeric_value_in_range(percent, (0, 100)) or not is_neither_npnan_nor_none(
        percent
    ):
        return True
    else:
        return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
def string_has_format_nnn_mmm(string: str) -> bool:
    if check_type_of_row(string, "str") and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
def datestring_has_format_yyyy_mm_dd(date: str) -> bool:
    if check_type_of_row(date, "str") and len(date) == 10:
        if date.find("-") == 4 and date.count("-") == 2:
            if 2100 >= int(date[:4]) >= 1900:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False
    return False


def is_valid_ratio_value_or_null(ratio: NUMERIC) -> bool:
    if is_numeric_value_in_range(ratio, (0.0, 1.0)) or not is_neither_npnan_nor_none(
        ratio
    ):
        return True
    else:
        return False


# for: gdf in soil_data_harmonization if has valid latitude
def is_valid_latitude(latitude: NUMERIC) -> bool:
    return is_numeric_value_in_range(latitude, (-90, 90))


# for: gdf in soil_data_harmonization if has valid longitude
def is_valid_longitude(longitude: NUMERIC) -> bool:
    return is_numeric_value_in_range(longitude, (-180, 180))


# for: dataset_geom_id if ID is valid
def check_positive_int(number: NUMERIC) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number >= 0 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number >= 0:
            return True
    return False


# for check_positive_int_or_null
def check_int_greater_zero(number: NUMERIC) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number > 0 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number > 0:
            return True
    return False


# for: every columns with an ID in upload_to_posgresql
def check_positive_int_or_Null(number: NUMERIC) -> bool:
    if not is_neither_npnan_nor_none(number):
        return True
    else:
        return check_int_greater_zero(number)


# for: check_positive_not_zero_float_or_null
def is_greater_zero_or_null(number: NUMERIC) -> bool:
    if not is_neither_npnan_nor_none(number):
        return True
    elif check_type_of_row(number, "float") or check_type_of_row(number, "int") is True:
        if number > 0:
            return True
    return False


# for: check_und_upload_samples, upload_to_postgresql
def check_string_available_for_database(db_string: str) -> bool:
    if check_type_of_row(db_string, "str"):
        if db_string.isalpha():
            return True
        else:
            regex = re.compile("^[^<>'\"/;`%]*$")
            if regex.search(db_string) is None or "_" in db_string:
                return True
    return False


# used for all range in is_valid_latitude, is_valid_longitude, is_valid_percent_value
def is_numeric_value_in_range(num_value: NUMERIC, num_range: Tuple[NUMERIC, NUMERIC]):
    if check_type_of_row(num_value, "float") or check_type_of_row(num_value, "int"):
        if num_range[0] <= num_value <= num_range[1]:
            return True
    return False
