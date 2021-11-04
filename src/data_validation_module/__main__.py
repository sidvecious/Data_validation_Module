"""
This is the main function,

with the functions that work with the dataframe or the columns
"""
import json
import sys
from collections.abc import Callable
from pathlib import Path, PosixPath
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from loguru import logger

from src.data_validation_module.row_validations import (
    check_int_greater_zero,
    check_positive_int,
    check_positive_int_or_Null,
    check_string_available_for_database,
    datestring_has_format_yyyy_mm_dd,
    is_greater_zero_or_null,
    is_neither_npnan_nor_none,
    is_string_represent_json,
    is_type_string,
    is_type_timestamp,
    is_valid_dir_path,
    is_valid_file_path,
    is_valid_latitude,
    is_valid_longitude,
    is_valid_percent_value_or_null,
    is_valid_ratio_value_or_null,
    string_has_format_nnn_mmm,
)

VALID_DATA = 1
INVALID_DATA = 0
VALID_DATA_COLUMN = "is_valid_data"
TYPES_IN_DICTIONARY_VALUES = Union[int, str, Path, PosixPath]


VALIDATION_DICT = {
    "datestring_has_format_yyyy_mm_dd": datestring_has_format_yyyy_mm_dd,
    "string_has_format_nnn_mmm": string_has_format_nnn_mmm,
    "check_int_greater_zero": check_int_greater_zero,
    "is_neither_npnan_nor_none": is_neither_npnan_nor_none,
    "is_valid_percent_value_or_null": is_valid_percent_value_or_null,
    "check_positive_int_or_Null": check_positive_int_or_Null,
    "check_positive_int": check_positive_int,
    "is_greater_zero_or_null": is_greater_zero_or_null,
    "check_string_available_for_database": check_string_available_for_database,
    "is_valid_latitude": is_valid_latitude,
    "is_valid_longitude": is_valid_longitude,
    "is_valid_ratio_value_or_null": is_valid_ratio_value_or_null,
    "is_type_timestamp": is_type_timestamp,
    "is_type_string": is_type_string,
    "is_string_represent_json": is_string_represent_json,
    "is_valid_dir_path": is_valid_dir_path,
    "is_valid_file_path": is_valid_file_path,
}


# this function load the json file with the complete configuration,
# and provides a config dictionary for the main validation function
def read_json_file(dataframe_config_path: Path) -> dict:
    with open(dataframe_config_path, "r+") as dfj:
        data_config = json.load(dfj)
    logger.info(f"{dataframe_config_path} id founded by read_json_file")
    return data_config


# for one column of the dataframe, iterate every row with the mapped function
def find_invalid_data_indices(
    series: pd.Series,
    mapped_function
    # mapped function is a function this this structure :
    # <function {name_of_function} at 0x00001e8D...
) -> List[int]:
    logger.info(f"called from dictionary:{mapped_function}")
    invalid_index_list = np.unique(
        np.where(series.apply(lambda x: not mapped_function(x)))
    ).tolist()
    return invalid_index_list


# DATAFRAME_DICT is the dictionary that I map all the validate functions
def validate_column(
    validation_function_name: str,
    series: pd.Series,
    validation_config: Optional[Dict[str, Callable]] = None,
) -> list:
    if not validation_config:
        validation_config = VALIDATION_DICT
    if validation_function_name in list(validation_config.keys()):
        validation_function = validation_config[validation_function_name]
        return find_invalid_data_indices(series, validation_function)
    else:
        logger.error(
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
            if column["name"] in df.columns:
                series = df[column["name"]]
                # a list is needed in this json position because for some data structures
                if type(column["validation"]) is not list:
                    logger.error(f'{column["validation"]} is wrong!')
                    continue
                for fn_name in column["validation"]:
                    # fn_name is the single validation function
                    invalid_index_list.extend(
                        validate_column(fn_name, series, VALIDATION_DICT)
                    )
                    invalid_index_list = list(set(invalid_index_list))

    return invalid_index_list


# final function: create the invalid_data csv and the cleaned dataframe with the validate rows
def split_invalid_data_rows(df: pd.DataFrame, output_csv_dir: Path) -> pd.DataFrame:
    logger.info(f"{len(df.index)} total rows in the DataFrame")
    df[df[VALID_DATA_COLUMN] == 0].to_csv(output_csv_dir / "invalid_rows.csv")
    df_clean = df[df[VALID_DATA_COLUMN] == 1]
    logger.info(f"{len(df_clean.index)} rows valid in the DataFrame")
    return df_clean


# main function for the dataframe, config_path is the name of the configuration Json
def check_dataframe(
    df_name: str, df: pd.DataFrame, dataframe_config_path: Path, output_csv_dir: Path
) -> pd.DataFrame:
    data_config = read_json_file(dataframe_config_path)
    invalid_index_list = iterate_data_config(df_name, data_config, df)
    logger.info(f"invalid_index_list: {invalid_index_list}")
    df[VALID_DATA_COLUMN] = VALID_DATA
    df.loc[invalid_index_list, VALID_DATA_COLUMN] = INVALID_DATA
    # df.invalid_data contains 1 in every invalid column, 0 in every valid column
    return split_invalid_data_rows(df, output_csv_dir)


def find_invalid_dict_values(
    table_name: str, mapped_function, target_value: TYPES_IN_DICTIONARY_VALUES
) -> list:
    # mapped function is a function this this structure :
    # <function {name_of_function} at 0x00001e8D...
    if mapped_function(target_value):
        logger.info(f"{target_value} is a correct {table_name} value")
        return []
    else:
        return [table_name]

    pass


def validate_functions_for_dictionaries(
    table_name: str,
    fn_name: str,
    target_value: TYPES_IN_DICTIONARY_VALUES,
    validation_config: Optional[Dict[str, Callable]] = None,
) -> list:
    if not validation_config:
        validation_config = VALIDATION_DICT
    if fn_name in list(validation_config.keys()):
        mapped_function = validation_config[fn_name]
        return find_invalid_dict_values(table_name, mapped_function, target_value)
    else:
        logger.error(f"warning: unable to find {fn_name} in the provided config.")
        return [table_name]


# print the invalid values of the target dictionary, for validate dictionaries
def print_invalid_dictionary(invalid_dict_values: list, output_dir: Path):
    invalid_dict_string = ", ".join(str(element) for element in invalid_dict_values)
    complete_path = output_dir / "invalid_dictionaries.txt"
    with open(complete_path, "w") as f:
        f.write(invalid_dict_string)


# iterate function for validate dictionaries
def iterate_dictionary_config(target_dict: dict, dict_name: str, data_config: dict):
    invalid_dict_values = []
    if dict_name in data_config:
        dict_config = data_config[dict_name]
        for constraint in dict_config["constraints"]:
            for rule in constraint["rules"]:
                for table_validation in rule:
                    fn_name = table_validation["validation"][0]
                    table_name = table_validation["table_name"]
                    try:
                        target_value = target_dict[table_name]
                    except KeyError:
                        logger.error(
                            f"target value {table_name} is not in the dictionary"
                        )
                        logger.error(
                            "check if the configuration file has the right table names"
                        )
                        sys.exit()
                    invalid_dict_values.extend(
                        validate_functions_for_dictionaries(
                            table_name, fn_name, target_value
                        )
                    )
    return invalid_dict_values


# main function for validate dictionaries
def check_dictionary(
    target_dict: dict, dict_name: str, dictionary_config_path: Path, output_dir: Path
):
    data_config = read_json_file(dictionary_config_path)
    invalid_dict_values = iterate_dictionary_config(target_dict, dict_name, data_config)
    if len(invalid_dict_values) > 0:
        logger.error(f"Invalid values in the dictionary: {invalid_dict_values}")
        print_invalid_dictionary(invalid_dict_values, output_dir)
    else:
        logger.info("Dictionary successfully validated")
    return target_dict
