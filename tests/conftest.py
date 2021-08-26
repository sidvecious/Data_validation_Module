import pandas as pd
import pytest


# test_data for test_df
@pytest.fixture(scope="module")
def test_data():
    return {
        "date_id": ["2200", "2001-01-01", "2002-02-02", "2003-03-03"],
        "depth_id": ["000_010", "000_010", "010_030", "888_000"],
    }


# is used in test_check_sample_gdf,
# and for create column test and control test
@pytest.fixture(scope="module")
def test_df():
    return pd.DataFrame(test_data)


# is used in test_check_sample_gdf
@pytest.fixture(scope="module")
def test_df_control(test_df):
    df = test_df.copy(deep=True)
    df.insert(2, "invalid_data", [1, 0, 0, 1])


# not used for the moment
# @pytest.fixture(scope="module")
# def test_df_with_invalid_column_empty(test_df):
#    df = test_df.copy(deep=True)
#    df['invalid_data'] = 0
#    return df


# used in test_check_dataset_depth_id_col
@pytest.fixture(scope="module")
def test_invalid_list_depth_id():
    return [3]


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
