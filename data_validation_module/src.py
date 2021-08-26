"""
Data_validation_module

A tool with different functions for the data validation

https://gitlab.com/cquest1/data_validation_module
"""
import numpy as np


def main():
    pass


def check_type_float(number):
    return True if isinstance(number, np.float64) else False


def check_range_from_zero_to_hundred(percent):
    if isinstance(percent, np.float64):
        if 0 <= percent <= 100:
            return True
    return False


def check_depth_string_zerofilled(top_limit, bottom_limit, depth):
    if type(depth) == str and len(depth) == 3 and depth.isnumeric():
        if top_limit <= depth <= bottom_limit:
            return True
    return False


def check_type_string(string):
    return True if isinstance(string, str) else False


def check_string_format_nnn_mmm(string):
    if type(string) == str and len(string) == 7 and string[3] == "_":
        top_depth = string[:3]
        bottom_depth = string[4:7]
        if top_depth.isnumeric() and bottom_depth.isnumeric():
            if float(top_depth) < float(bottom_depth):
                return True
    return False


def check_date_format_YYYY_mm_dd(date):
    pass


def check_dataset_depth_id_col(invalid_list, depht_id_column):
    pass


def check_dataset_date_id_col(invalid_list, date_id_column):
    pass


def check_sample_gdf(gdf):
    pass


def split_invalid_data_rows(df, data_dir):
    pass


if __name__ == "__main__":
    main()
