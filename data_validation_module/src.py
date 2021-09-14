"""
This is the main function,

with the functions that work with the dataframe or the columns
"""
import json
import numpy as np
import pandas as pd

# OPEN QUESTION 1
# the program still need this 3 function, but I don't understand why
from data_validation_module.data_validation_module.row_validations import (  # check_double_90,; check_double_180,; check_positive_int,; check_positive_int_or_Null,; check_range_from_zero_to_hundred,; check_string_available_for_database,
    check_date_format_YYYY_mm_dd,
    check_string_format_nnn_mmm,
    check_type_of_row,
)
from file_path_tools.search_and_find import find_closest_filepath
from loguru import logger


# this function load the json file with the complete configuration,
# and give a dictionary for the function main
def read_json_file(dataframe_dictionary: str) -> dict:
    with open(find_closest_filepath(dataframe_dictionary)) as dfj:
        data_config = json.load(dfj)
    return data_config


# for one column of the datatframe, iterate every row with the mapped function
def iterate_column(
    series: pd.Series,
    mapped_function,
    type_series: str
    # mapped function is a function this this structure :
    # <function {name_of_function} at 0x00001e8D...
) -> list:
    invalid_list = np.unique(
        np.where(series.apply(lambda x: not mapped_function(x, type_series)))
    )
    return invalid_list


# this is in origin part of iterate_data_config,
# and i splitted because data config is too big and has too many functionality
# DATAFRAME_DICT is the dictionary that I map all the validate functions
# THIS FUNCTION HASN'T TEST
def validate_column(
    df_name: str, fn_name: str, series: pd.Series, type_series: str
) -> list:
    from data_validation_module.data_validation_module.dictionaries import (
        DATAFRAME_DICT,
    )

    if fn_name in DATAFRAME_DICT:
        mapped_function = DATAFRAME_DICT[fn_name]
        return iterate_column(series, mapped_function, type_series)
    else:
        logger.info(f"warning: unable to find {fn_name} for {df_name}")
        return []


# this function iterate through the dataframe_config, and check if the df exist
# also iterate through the df and iterate the column,
# OPEN QUESTION 2: maybe i must split also this function because has two different functionality
def iterate_data_config(df_name: str, dataframe_config: dict, df: pd.DataFrame) -> list:
    from data_validation_module.data_validation_module.dictionaries import (
        DATAFRAME_DICT,
    )

    invalid_list = []
    if df_name in dataframe_config:
        df_config = dataframe_config[df_name]
        for column in df_config["columns"]:
            type_series = column[
                "type"
            ]  # is a string with the expected type of the Series
            series = df[column["name"]]
            # I need a list in this json position because for some data structures
            # more of one check ins needed
            if type(column["validation"]) is not list:
                logger.info(f'{column["validation"]} is wrong!')
                continue
            for fn_name in column[
                "validation"
            ]:  # fn_name is the single validation function
                invalid_list.extend(
                    validate_column(df_name, fn_name, series, type_series)
                )
                invalid_list = list(set(invalid_list))

    return invalid_list


# final function: create the invalid_data csv and the cleaned dataframe with the validate rows
def split_invalid_data_rows(df: pd.DataFrame) -> pd.DataFrame:
    data_dir = find_closest_filepath("data_validation_module/test_files")
    df[df.invalid_data == 1].to_csv(data_dir / "invalid_rows.csv")
    return df[df.invalid_data == 0]


# main function for the dataframe, config_path is the name of the configuration Json
def check_dataframe(df_name: str, df: pd.DataFrame, config_path: str) -> pd.DataFrame:
    data_config = read_json_file(config_path)
    # invalid_list is a list with the index of all the invalid rows
    invalid_list = iterate_data_config(df_name, data_config, df)
    valid_data = 0
    if "invalid_data" not in df:
        df["invalid_data"] = valid_data
    invalid_data = 1
    df.loc[invalid_list, "invalid_data"] = invalid_data
    # df.invalid_data contains 1 in every invalid column, 0 for every valid column
    return split_invalid_data_rows(df)
