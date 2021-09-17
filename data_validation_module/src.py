"""
This is the main function,

with the functions that work with the dataframe or the columns
"""
import json
from collections.abc import Callable
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from data_validation_module.row_validations import (
    check_double_90,
    check_double_180,
    check_npnan_nor_none,
    check_positive_int,
    check_positive_int_from_one,
    check_positive_int_or_Null,
    check_positive_not_zero_float_or_null,
    check_range_from_zero_to_hundred,
    check_string_available_for_database,
    check_string_format_nnn_mmm,
    check_type_of_row,
    datestring_has_format_yyyy_mm_dd,
)
from file_path_tools.search_and_find import find_closest_filepath
from loguru import logger

VALID_DATA = 1
INVALID_DATA = 0
VALID_DATA_COLUMN = "is_valid_data"


DATAFRAME_DICT = {
    "datestring_has_format_yyyy_mm_dd": datestring_has_format_yyyy_mm_dd,
    "check_string_format_nnn_mmm": check_string_format_nnn_mmm,
    "check_type_of_row": check_type_of_row,
    "check_positive_int_from_one": check_positive_int_from_one,
    "check_npnan_nor_none": check_npnan_nor_none,
    "check_range_from_zero_to_hundred": check_range_from_zero_to_hundred,
    "check_positive_int_or_Null": check_positive_int_or_Null,
    "check_positive_int": check_positive_int,
    "check_positive_not_zero_float_or_null": check_positive_not_zero_float_or_null,
    "check_string_available_for_database": check_string_available_for_database,
    # not tested!
    "check_double_90": check_double_90,
    "check_double_180": check_double_180,
}


# this function load the json file with the complete configuration,
# and give a dictionary for the function main
def read_json_file(dataframe_config_file_name: str) -> dict:
    with open(find_closest_filepath(dataframe_config_file_name)) as dfj:
        data_config = json.load(dfj)
    logger.info(f"{dataframe_config_file_name} id founded by read_json_file")
    return data_config


# for one column of the dataframe, iterate every row with the mapped function
def find_invalid_data_indices(
    series: pd.Series,
    mapped_function,
    type_series: str
    # mapped function is a function this this structure :
    # <function {name_of_function} at 0x00001e8D...
) -> List[int]:
    logger.debug(mapped_function)
    invalid_index_list = np.unique(
        np.where(series.apply(lambda x: not mapped_function(x, type_series)))
    ).tolist()
    return invalid_index_list


# this is in origin part of iterate_data_config,
# and i split because data config is too big and has too many functionality
# DATAFRAME_DICT is the dictionary that I map all the validate functions
def validate_column(
    validation_function_name: str,
    series: pd.Series,
    type_series: str,
    validation_config: Optional[Dict[str, Callable]] = None,
) -> list:
    # logger.info(f"fn_name: {fn_name}")
    # logger.info(f"fn_name: {type(fn_name)}")
    # logger.info(f"dict: {DATAFRAME_DICT} ")
    if not validation_config:
        validation_config = DATAFRAME_DICT
    if validation_function_name in list(validation_config.keys()):
        validation_function = validation_config[validation_function_name]
        return find_invalid_data_indices(series, validation_function, type_series)
    else:
        logger.info(
            f"warning: unable to find {validation_function_name} in the provided config."
        )
        return []


# this function iterate through the dataframe_config, and check if the df exist
# also iterate through the df and iterate the column
def iterate_data_config(
    df_name: str, dataframe_config: dict, df: pd.DataFrame
) -> List[int]:
    invalid_index_list = []
    if df_name in dataframe_config:
        df_config = dataframe_config[df_name]
        for column in df_config["columns"]:
            type_series = column["type"]
            # is the expected type of the Series in string
            series = df[column["name"]]
            # I need a list in this json position because for some data structures
            # more of one check ins needed
            if type(column["validation"]) is not list:
                logger.info(f'{column["validation"]} is wrong!')
                continue
            for fn_name in column["validation"]:
                # fn_name is the single validation function
                invalid_index_list.extend(
                    validate_column(fn_name, series, type_series, DATAFRAME_DICT)
                )
                invalid_index_list = list(set(invalid_index_list))

    return invalid_index_list


# final function: create the invalid_data csv and the cleaned dataframe with the validate rows
def split_invalid_data_rows(df: pd.DataFrame, output_csv_dir: str) -> pd.DataFrame:
    data_dir = find_closest_filepath(output_csv_dir)
    logger.info(f"{len(df.index)} total rows in the DataFrame")
    df[df[VALID_DATA_COLUMN] == 0].to_csv(data_dir / "invalid_rows.csv")
    df_clean = df[df[VALID_DATA_COLUMN] == 1]
    logger.info(f"{len(df_clean.index)} rows valid in the DataFrame")
    return df_clean


# main function for the dataframe, config_path is the name of the configuration Json
def check_dataframe(
    df_name: str, df: pd.DataFrame, dataframe_config_file_name: str, output_csv_dir: str
) -> pd.DataFrame:
    data_config = read_json_file(dataframe_config_file_name)
    # invalid_list is a list with the index of all the invalid rows
    invalid_index_list = iterate_data_config(df_name, data_config, df)
    logger.info(f"invalid_index_list: {invalid_index_list}")
    df[VALID_DATA_COLUMN] = VALID_DATA
    df.loc[invalid_index_list, VALID_DATA_COLUMN] = INVALID_DATA
    # df.invalid_data contains 1 in every invalid column, 0 for every valid column
    return split_invalid_data_rows(df, output_csv_dir)
