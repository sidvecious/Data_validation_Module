import json

import pandas as pd
import pytest
from file_path_tools.search_and_find import find_closest_filepath


# test_data for test_df
@pytest.fixture(scope="module")
def test_data():
    return {
        "date_id": ["2200", "2001-01-01", "2002-02-02", "2003-03-03"],
        "depth_id": ["000_010", "888_000", "000_030", "000_040"],
        "soil_texture": ["sands", "silts", 52, "clays"],
    }


# is used in ...,
# and for create column test and test_df_with_invalid_rows
@pytest.fixture(scope="module")
def test_df():
    return pd.DataFrame(test_data)


# is used in test_check_sample_gdf
@pytest.fixture(scope="module")
def test_df_with_invalid_column_filled(test_df):
    df = test_df.copy(deep=True)
    df.insert(2, "invalid_data", [1, 1, 1, 0])


@pytest.fixture(scope="module")
def test_valid_df(test_df):
    valid_df = test_df.copy(deep=True)
    valid_df.drop([0, 1, 2], inplace=True)
    return valid_df()


@pytest.fixture(scope="module")
def test_invalid_df(test_df):
    invalid_df = test_df.copy(deep=True)
    invalid_df.drop([4], inplace=True)
    return invalid_df()


# not used for the moment
# @pytest.fixture(scope="module")
# def test_df_with_invalid_column_empty(test_df):
#    df = test_df.copy(deep=True)
#    df['invalid_data'] = 0
#    return df


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_invalid_list_depth_id():
    return [1]


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_depth_id_column(test_df):
    return test_df.depth_id


# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_invalid_list_date_id():
    return [0]


# used in test_check_date_id_col
@pytest.fixture(scope="module")
def test_date_id_column(test__df):
    return test_df.date_id


# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_invalid_soil_texture():
    return [2]


# used in test_check_soil_texture_col
@pytest.fixture(scope="module")
def test_soil_texture_column(test_df):
    return test_df.soil_texture


@pytest.fixture(scope="module")
def test_data_config():
    return {
        "test_df": {
            "date_id": "date_id",
            "geom_id": "geom_id",
            "soil_texture": "soil_texture",
        }
    }


@pytest.fixture(scope="module")
def test_df_name_control():
    return "test_df"


@pytest.fixture(scope="module")
def test_invalid_data():
    return [1, 1, 1, 0]


@pytest.fixture(scope="module")
def test_string_dataframe_config_json():
    return "test_dataframe_config.json"
