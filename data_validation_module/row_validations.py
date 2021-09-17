"""
file with the row validation functions
"""

import re
from datetime import datetime

import numpy as np
from loguru import logger

# General TODOs
# TODO: please add type hints/ checks for all function headers.
# TODO: find better names for variables/parameters than "data"


# TODO: spell out (in a comment or function docstring) which values data_type can have: "str", "int", other?
#  There could even be an assert statement at the beginning, to check that data_type is in ["str", "int", etc.]
# the basic function for every type check accept bool, none, nan, str, int, float and Timestamp
# It should accept any other class
def check_type_of_row(row_item, row_item_type) -> bool:
    try:
        return type(row_item).__name__ == row_item_type
    except Exception as err:
        logger.error(f"something is wrong with {row_item}, {row_item_type}, {err}")
        return False


# returns False for np.NaN values for data
# is called only when the expected type is an instance of numpy
# for exclude np.NaN
# TODO: rename to is_neither_npnan_nor_none, parameter "_data_type" not used
def check_npnan_nor_none(row_item, _):
    # logger.info(f"data: {data}")
    if check_type_of_row(row_item, "float") and np.isnan(row_item):
        return False
    elif row_item is None:
        return False
    # this code is comment now but could be necessary if we want exclude also None
    return True


# for: upload_ready_data, in the target columns with 'percent'
# the function accept type int and float
# TODO: rename to percentage_value_in_range_0_100, data_type here should be "float" or "int", right?
def check_range_from_zero_to_hundred(percent, _) -> bool:
    if check_type_of_row(percent, "float") or check_type_of_row(percent, "int"):
        if 0.0 <= percent <= 100.0:
            return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
# the function accept type str
# TODO: data_type here should always be "str", right?
def check_string_format_nnn_mmm(string: str, _) -> bool:
    if check_type_of_row(string, "str") and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
# the function accept type str
# TODO: maybe rename to datestring_has_format_yyyy_mm_dd, data_type here should always be "str", right?
def datestring_has_format_yyyy_mm_dd(date: str, _) -> bool:
    if check_type_of_row(date, "str") and len(date) == 10:
        if date.find("-") == 4 and date.count("-") == 2:
            if 2100 >= int(date[:4]) >= 1900:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False
    return False


# TODO: the following functions are duplicates, the only difference is the value range,
#  maybe this can be turned into one single function with two implementations.
# for: gdf in soil_data_harmonization, lat_col must have float64 between -90 and 90
# the function accept type float and int
# TODO: data_type here should be "float" or "int", right?
def check_double_90(coord, _) -> bool:
    if check_type_of_row(coord, "float") or check_type_of_row(coord, "int"):
        if -90 <= coord <= 90:
            return True
    return False


# for: gdf in soil_data_harmonization, lon_col must have float64 between -180 and 180
# the function accept type float and int
# TODO: data_type here should be "float" or "int", right?
def check_double_180(coord, _) -> bool:
    if check_type_of_row(coord, "float") or check_type_of_row(coord, "int"):
        if -180 <= coord <= 180:
            return True
    return False


# for: dataset_geom_id
# the function accept type float and int
# TODO: "data_type" unused.
def check_positive_int(number, _) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number >= 0 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number >= 0:
            return True
    return False


# for check_positive_int_or_null
# the function accept type float and int
# TODO: "data_type" unused.
def check_positive_int_from_one(number, _) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number >= 1 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number >= 1:
            return True
    return False


# for: every columns with an ID in upload_to_posgresql
# the function accept type float and int
def check_positive_int_or_Null(number, _) -> bool:
    if check_npnan_nor_none(number, _) is False:
        return True
    else:
        return check_positive_int_from_one(number, _)


# for: check_positive_not_zero_float_or_null
# this type of column could have float, int or null
def check_positive_not_zero_float_or_null(number, _) -> bool:
    if check_npnan_nor_none(number, _) is False:
        return True
    elif check_type_of_row(number, "float") or check_type_of_row(number, "int") is True:
        if number > 0:
            return True
    return False


# for: check_und_upload_samples, upload_to_postgresql
# TODO: data_type here should always be "str", right?
# the function accept type str
def check_string_available_for_database(db_string, _) -> bool:
    if check_type_of_row(db_string, "str"):
        if db_string.isalpha():
            return True
        else:
            regex = re.compile("^[^<>'\"/;`%]*$")
            if regex.search(db_string) is None or "_" in db_string:
                return True
    return False
