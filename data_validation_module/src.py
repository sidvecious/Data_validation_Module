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
        if string[:3].isnumeric() and string[4:7].isnumeric():
            return True
    return False


if __name__ == "__main__":
    main()
