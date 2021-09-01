"""
Data_validation_module

A tool with different functions for the data validation

https://gitlab.com/cquest1/data_validation_module
"""

from datetime import datetime

import numpy as np
import pandas as pd


def main():
    pass


def check_type_of_row(data, type) -> bool:
    return True if isinstance(data, type) else False


def check_range_from_zero_to_hundred(percent) -> bool:
    if isinstance(percent, np.float64):
        if 0 <= percent <= 100:
            return True
    return False


def check_depth_string_zerofilled(
    top_limit: str, bottom_limit: str, depth: str
) -> bool:
    if type(depth) == str and len(depth) == 3 and depth.isnumeric():
        if top_limit <= depth <= bottom_limit:
            return True
    return False


# unite check_type_string and heck_type_float in the same function
# def check_type_string(string):
#    return isinstance(string, str)


def check_string_format_nnn_mmm(string: str) -> bool:
    if type(string) == str and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


def check_date_format_YYYY_mm_dd(date: str) -> bool:
    if type(date) == str and len(date) == 10:
        if date.find("-") == 4 and date.count("-") == 2:
            if 2100 >= int(date[:4]) >= 1900:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False
    return False


def check_double_90_180(coordinate, axis) -> bool:
    pass


def check_date_format_or_NaT(date) -> bool:
    pass


def check_string_format_nnn_mmm_with_NA(string) -> bool:
    pass


def check_range_0_100(percent) -> bool:
    pass


def check_positive_int(number) -> bool:
    pass


def check_positive_int_or_Null(value) -> bool:
    pass


def check_string_available_for_database(string) -> bool:
    pass


# def check_depth_string_zerofilled_or_NA(depth) -> bool:
#    pass


def read_json_file(dataframe_dictionary: str) -> dict:
    pass


def get_df_name(df: pd.DataFrame) -> str:
    pass


def iterate_data_config(df_name: str, data_config: dict, df: pd.DataFrame) -> list:
    pass


def iterate_column(series: pd.Series, mapped_function: str) -> list:
    pass


def split_invalid_data_rows(df: pd.DataFrame) -> pd.DataFrame:
    pass


def check_dataframe(df: pd.DataFrame, dataframe_dictionary: str) -> pd.DataFrame:
    pass


if __name__ == "__main__":
    main()
