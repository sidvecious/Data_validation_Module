import re
from datetime import datetime

import numpy as np
from loguru import logger


# the basic function for every type check
def check_type_of_row(data, data_type) -> bool:
    try:
        return type(data).__name__ == data_type
    except Exception as err:
        logger.error(f"something is wrong with {data}, {data_type}, {err}")
        return False


# this function dela with the np.NaN is called only when the expected type is an instance of numpy
def check_none(data, _type_data):
    return not np.isnan(data)


# for: upload_ready_data, in the target columns with 'percent'
def check_range_from_zero_to_hundred(percent, data_type) -> bool:
    if check_type_of_row(percent, data_type):
        if 0 <= percent <= 100:
            return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
def check_string_format_nnn_mmm(string: str, data_type) -> bool:
    if check_type_of_row(string, data_type) and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


# for: upload_ready_data, check_und_upload_geometry, check_und_upload_samples
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


# for: gdf in soil_data_harmonization, lat_col must have float64 between -90 and 90
def check_double_90(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        if -90 <= number <= 90:
            return True
    return False


# for: gdf in soil_data_harmonization, lon_col must have float64 between -180 and 180
def check_double_180(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        if -180 <= number <= 180:
            return True
    return False


# for: dataset_geom_id
def check_positive_int(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        if number >= 1:
            return True
    return False


# for: every columns with an ID in upload_to_posgresql
def check_positive_int_or_Null(number, data_type) -> bool:
    if check_type_of_row(number, data_type):
        return True if number >= 1 else False
    elif number is None:
        return True
    else:
        return False


# for: check_und_upload_samples, upload_to_postgresql
def check_string_available_for_database(string, data_type) -> bool:
    if check_type_of_row(string, data_type):
        regex = re.compile("^[^<>'\"/;`%]*$")
        if regex.search(string) is None or "_" in string:
            return True
    return False
