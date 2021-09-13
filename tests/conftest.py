import pandas as pd
import pytest


# test_data for test_df
@pytest.fixture(scope="module")
def test_data():
    return {
        "date_id": ["2200", "2001-01-01", "2002-02-02", "2003-03-03"],
        "depth_id": ["000_010", "888_000", "000_030", "000_040"],
        "soil_texture": ["sands", "silts", 52, "clays"],
    }


# is used in test_iterate_data_config
# and for create column test and test_df_with_invalid_rows
@pytest.fixture(scope="module")
def test_df(test_data):
    test_df = pd.DataFrame(test_data)
    return test_df


# is used in test_check_sample_gdf
@pytest.fixture(scope="module")
def test_df_with_invalid_column_filled(test_df):
    df = test_df.copy(deep=True)
    df.insert(2, "invalid_data", [1, 1, 1, 0])


# is used in test_split_invalid_data_row_1
@pytest.fixture(scope="module")
def test_valid_df(test_df):
    valid_df = test_df.copy(deep=True)
    valid_df.drop([0, 1, 2], inplace=True)
    return valid_df()


# is used in test_split_invalid_data_row_0
@pytest.fixture(scope="module")
def test_invalid_df(test_df):
    invalid_df = test_df.copy(deep=True)
    invalid_df.drop([4], inplace=True)
    return invalid_df()


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_invalid_list_depth_id():
    return [1]


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_depth_id_column(test_df):
    df = test_df.copy(deep=True)
    return df.depth_id


# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_invalid_list_date_id():
    return [0]


# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_date_id_column(test_df):
    df = test_df.copy(deep=True)
    return df.date_id


# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_invalid_soil_texture():
    return [2]


# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_soil_texture_column(test_df):
    df = test_df.copy(deep=True)
    return df.soil_texture


# is used in test_iterate_data_config and test_read_json_file
# the structure of json is:
# single dataframe-> columns of dataframe -> name, type, validation function
@pytest.fixture(scope="module")
def test_dataframe_config():
    return {
        "test_df": {
            "columns": [
                {
                    "name": "date_id",
                    "type": "str",
                    "validation": ["check_date_format_YYYY_mm_dd"],
                },
                {
                    "name": "depth_id",
                    "type": "str",
                    "validation": ["check_string_format_nnn_mmm"],
                },
                {
                    "name": "soil_texture",
                    "type": "str",
                    "validation": ["check_type_of_row"],
                },
            ]
        },
        "test_df2": {
            "columns": [
                {
                    "name": "date_id",
                    "type": "str",
                    "validation": "check_date_format_YYYY_mm_dd",
                },
                {"name": "depth_id", "type": "str", "validation": "check_positive_int"},
            ]
        },
    }


# used in test_iterate_data_config, test_check_dataframe
@pytest.fixture(scope="module")
def test_df_name():
    return "test_df"


# used in test_split_invalid_data_row_0
@pytest.fixture(scope="module")
def test_invalid_list():
    return [1, 1, 1, 0]


# used in test_read_json_file
@pytest.fixture(scope="module")
def test_string_dataframe_config_json():
    return "test_dataframe_config.json"


# used in test_check_dataset_depth_id_col_0,
# test_check_date_id_col_0,
# test_check_soil_texture_col_0
@pytest.fixture(scope="module")
def test_mapped_function():
    from data_validation_module.data_validation_module.dictionaries import (
        DATAFRAME_DICT,
    )

    return DATAFRAME_DICT
