import copy
import json
from pathlib import Path

import pandas as pd
import pytest

from src.data_validation_module.__main__ import VALID_DATA_COLUMN, VALIDATION_DICT


# test_data for test_df
@pytest.fixture(scope="module")
def test_data():
    return {
        "date_id": ["2200", "2001-01-01", "2002-02-02", "2003-03-03", "2004-04-04"],
        "depth_id": ["000_010", "888_000", "000_020", "000_030", "000_040"],
        "soil_texture": ["sands", "silts", 52, "clays", "rocky"],
        "db_id": [1, 2, 3, "aaa", 5],
    }


# is used in test_iterate_data_config
# and for create column test and test_df_with_invalid_rows
@pytest.fixture(scope="module")
def test_df(test_data):
    test_df = pd.DataFrame(test_data)
    return test_df


@pytest.fixture(scope="module")
def test_invalid_index_list():
    return [0, 1, 2, 3]


@pytest.fixture(scope="module")
def test_only_valid_index():
    return 4


# used in test_split_invalid_data_row_0, test_check_sample_gdf
@pytest.fixture(scope="module")
def test_valid_data_column():
    return [0, 0, 0, 0, 1]


# is used in test_check_sample_gdf
@pytest.fixture(scope="module")
def test_df_with_invalid_column_filled(test_df, test_valid_data_column):
    df = test_df.copy(deep=True)
    df.insert(2, VALID_DATA_COLUMN, test_valid_data_column)
    return df


# is used in test_split_invalid_data_row_1
@pytest.fixture(scope="module")
def test_valid_df(test_df, test_invalid_index_list):
    valid_df = test_df.copy(deep=True)
    valid_df.drop(test_invalid_index_list, inplace=True)
    valid_df[VALID_DATA_COLUMN] = 1
    return valid_df


# is used in test_split_invalid_data_row_0
@pytest.fixture(scope="module")
def test_invalid_df(test_df, test_only_valid_index):
    invalid_df = test_df.copy(deep=True)
    invalid_df.drop([test_only_valid_index], inplace=True)
    invalid_df[VALID_DATA_COLUMN] = 0
    return invalid_df


# --- depth_id ---
# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_invalid_list_depth_id():
    return [1]


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_depth_id_column(test_df):
    df = test_df.copy(deep=True)
    return df.depth_id


# used in test_check_dataset_depth_id_col_0,
@pytest.fixture(scope="module")
def test_depth_id_function_name():
    return "string_has_format_nnn_mmm"


# --- date_id ---
# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_invalid_list_date_id():
    return [0]


# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_date_id_column(test_df):
    df = test_df.copy(deep=True)
    return df.date_id


# used in test_check_dataset_date_id_col_0,
@pytest.fixture(scope="module")
def test_date_id_function_name():
    return "datestring_has_format_yyyy_mm_dd"


# --- soil_texture ---
# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_invalid_soil_texture():
    return [2]


# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_soil_texture_column(test_df):
    df = test_df.copy(deep=True)
    return df.soil_texture


# used in test_check_soil_texture_col_0,
@pytest.fixture(scope="module")
def test_is_type_string_function_name():
    return "is_type_string"


# --- db_id ---
@pytest.fixture(scope="module")
def test_db_id_function_name():
    return "check_positive_int"


@pytest.fixture(scope="module")
def test_invalid_list_db_id():
    return [3]


@pytest.fixture(scope="module")
def test_db_id_column(test_df):
    df = test_df.copy(deep=True)
    return df.db_id


# test_df is used in test_iterate_data_config and test_read_json_file
# single_column_test is used for test find_invalid_data_indices, with mark parametrize
# the structure of json is:
# single dataframe-> columns of dataframe -> name, type, validation function
@pytest.fixture(scope="module")
def test_dataframe_config():
    return {
        "test_df": {
            "columns": [
                {"name": "date_id", "validation": ["datestring_has_format_yyyy_mm_dd"]},
                {"name": "depth_id", "validation": ["string_has_format_nnn_mmm"]},
                {"name": "soil_texture", "validation": ["is_type_string"]},
                {
                    "name": "db_id",
                    "validation": ["is_neither_npnan_nor_none", "check_positive_int"],
                },
            ]
        }
    }


# used in test_iterate_data_config, test_check_dataframe
@pytest.fixture(scope="module")
def test_df_name():
    return "test_df"


# used in test_read_json_file
@pytest.fixture(scope="module")
def test_dataframe_config_path():
    return Path("test_files/test_dataframe_config.json")


# used in test_check_dataset_depth_id_col_0,
# test_check_date_id_col_0,
# test_check_soil_texture_col_0
@pytest.fixture(scope="module")
def test_mapped_function():
    return VALIDATION_DICT


# used for test_split_invalid_data_row_0, test_split_invalid_data_row_1,
# test_check_dataframe, test_print_invalid_dictionary, test_check_dictionary_right
# test_check_dictionary_wrong_values, est_check_dictionary_wrong_keys
@pytest.fixture(scope="module")
def test_output_dir():
    return Path("test_files")


# used for all the test of:
# iterate_dictionary_config, print_invalid_dictionary, check_dictionary
@pytest.fixture(scope="module")
def test_target_dict_right():
    return {
        "database_id": 7,
        "db_string": "str1ng_with_number",
        "dir_path": Path("test_files"),
        "file_path": Path("test_files/test_json.json"),
        "json_file": "json_file.json",
    }


# used in: test_iterate_dictionary_config_wrong_database_id,
# test_iterate_dictionary_config_wrong_db_id_and_string,
# test_check_dictionary_wrong_values
@pytest.fixture(scope="module")
def test_target_dict_wrong_database_id(test_target_dict_right):
    new_dict = copy.deepcopy(test_target_dict_right)
    new_dict["database_id"] = -7
    return new_dict


# used in: test_check_dictionary_wrong_values
# test_iterate_dictionary_config_wrong_db_id_and_string
@pytest.fixture(scope="module")
def test_target_dict_wrong_db_id_and_string(test_target_dict_wrong_database_id):
    new_dict = copy.deepcopy(test_target_dict_wrong_database_id)
    new_dict["db_string"] = "%^&"
    return new_dict


# used in: test_check_dictionary_with_wrong_key
# test_iterate_dictionary_config_wrong_key
@pytest.fixture(scope="module")
def test_target_dict_wrong_key(test_target_dict_right):
    new_dict = copy.deepcopy(test_target_dict_right)
    new_dict["wrong_key"] = new_dict.pop("database_id")
    return new_dict


# used in all tests of the function: iterate_dictionary_config
@pytest.fixture(scope="module")
def test_config_dictionary():
    dictionary_config_path = "test_files/test_dictionary_config.json"
    with open(dictionary_config_path, "r+") as dfj:
        data_config = json.load(dfj)
    return data_config


# used in all tests of check_dictionary,
@pytest.fixture(scope="module")
def test_dict_name():
    return "test_target_dict"


# used in all tests of check_dictionary, iterate_dictionary_config
@pytest.fixture(scope="module")
def test_dictionary_config_path():
    return Path("test_files/test_dictionary_config.json")
