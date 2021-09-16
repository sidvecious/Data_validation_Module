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
# the basic function for every type check
def check_type_of_row(data, data_type) -> bool:
    try:
        return type(data).__name__ == data_type
    except Exception as err:
        logger.error(f"something is wrong with {data}, {data_type}, {err}")
        return False


# returns False for np.NaN values for data
# is called only when the expected type is an instance of numpy
# for exclude np.NaN
# TODO: rename to is_neither_npnan_nor_none, parameter "_data_type" not used
def check_none_and_nan(data, _data_type):
    # logger.info(f"data: {data}")
    if check_type_of_row(data, "float") and np.isnan(data):
        return False
    elif data is None:
        return False
    # this code is comment now but could be necessary if we want exclude also None
    return True


# for: upload_ready_data, in the target columns with 'percent'
# TODO: rename to percentage_value_in_range_0_100, data_type here should be "float" or "int", right?
def check_range_from_zero_to_hundred(percent, data_type) -> bool:
    if check_type_of_row(percent, data_type):
        if 0.0 <= percent <= 100.0:
            return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
# TODO: data_type here should always be "str", right?
def check_string_format_nnn_mmm(string: str, data_type) -> bool:
    if check_type_of_row(string, data_type) and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
# TODO: maybe rename to datestring_has_format_yyyy_mm_dd, data_type here should always be "str", right?
def check_date_format_YYYY_mm_dd(date: str, data_type) -> bool:
    if check_type_of_row(date, data_type) and len(date) == 10:
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
# TODO: data_type here should be "float" or "int", right?
def check_double_90(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        if -90 <= number <= 90:
            return True
    return False


# for: gdf in soil_data_harmonization, lon_col must have float64 between -180 and 180
# TODO: data_type here should be "float" or "int", right?
def check_double_180(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        if -180 <= number <= 180:
            return True
    return False


# for: dataset_geom_id
# TODO: "data_type" unused.
def check_positive_int(number, _data_type) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number >= 0 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number >= 0:
            return True
    return False


# for check_positive_int_or_null
# TODO: "data_type" unused.
def check_positive_int_from_one(number, _data_type) -> bool:
    if check_type_of_row(number, "float"):
        if number is not np.isnan(number):
            if number >= 1 and number.is_integer():
                return True
    elif check_type_of_row(number, "int"):
        if number >= 1:
            return True
    return False


# for: every columns with an ID in upload_to_posgresql
def check_positive_int_or_Null(number, data_type) -> bool:
    # logger.info(f"number: {number}")
    # logger.info(f"data_type: {data_type}")
    # logger.info(f"type of number {type(number)}")
    if check_none_and_nan(number, data_type) is False:
        return True
    else:
        return check_positive_int_from_one(number, data_type)


# for: check_und_upload_samples, upload_to_postgresql
# TODO: data_type here should always be "str", right?
def check_string_available_for_database(string, data_type) -> bool:
    if check_type_of_row(string, data_type):
        regex = re.compile("^[^<>'\"/;`%]*$")
        if regex.search(string) is None or "_" in string:
            return True
    return False
