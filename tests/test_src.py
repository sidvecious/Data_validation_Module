import os

import numpy as np
import pandas as pd
import pytest
from data_validation_module.src import (
    check_dataframe,
    find_invalid_data_indices,
    iterate_data_config,
    read_json_file,
    split_invalid_data_rows,
    validate_column,
)
from file_path_tools.search_and_find import find_closest_filepath
from loguru import logger


# test of iterate_column with the depth_id column
def test_check_dataset_depth_id_col_0(
    test_depth_id_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_list_depth_id: list,
    test_depth_id_function_name: str,
):
    result = find_invalid_data_indices(
        test_depth_id_column, test_mapped_function[test_depth_id_function_name]
    )
    assert result == test_invalid_list_depth_id


# test of iterate column with date_id column
def test_check_date_id_col_0(
    test_date_id_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_list_date_id: list,
    test_date_id_function_name: str,
):
    result = find_invalid_data_indices(
        test_date_id_column, test_mapped_function[test_date_id_function_name]
    )
    assert result == test_invalid_list_date_id


# test of iterate column with a string column
def test_check_soil_texture_col_0(
    test_soil_texture_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_soil_texture: list,
    test_is_type_string_function_name: str,
):
    result = find_invalid_data_indices(
        test_soil_texture_column,
        test_mapped_function[test_is_type_string_function_name],
    )
    assert result == test_invalid_soil_texture


# test of iterate_column with the depth_id column
def test_check_dataset_db_id_col(
    test_db_id_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_list_db_id: list,
    test_db_id_function_name: str,
):
    invalid_result = find_invalid_data_indices(
        test_db_id_column, test_mapped_function[test_db_id_function_name]
    )
    assert invalid_result == test_invalid_list_db_id


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"soc_percent": [1, 2.2, 103.3]}), [2]),
        (pd.DataFrame({"soc_percent": [1, 2.2, -2.3]}), [2]),
        (pd.DataFrame({"soc_percent": [1.1, None, 3.3]}), [1]),
        (pd.DataFrame({"soc_percent": [np.NaN, 2.2, 3.3]}), [0]),
        (pd.DataFrame({"soc_percent": ["string", 2.2, 3.3]}), [0]),
        (pd.DataFrame({"soc_percent": [True, 1.1, 2.2]}), [0]),
    ],
)
def test_is_valid_percent_value_col(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.soc_percent
    test_function = DATAFRAME_DICT["is_valid_percent_value"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"db_id": [1, 0, -3]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, -3]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, "aaa"]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, None]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, np.NaN]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, True]}), [2]),
        (pd.DataFrame({"db_id": [1, 2, 3.3]}), [2]),
    ],
)
def test_check_dataset_db_id_col2(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.db_id
    test_function = DATAFRAME_DICT["check_positive_int"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"bulk_density": [1.23, None, "aaa"]}), [2]),
        (pd.DataFrame({"bulk_density": [1.23, np.NaN, "aaa"]}), [2]),
        (pd.DataFrame({"bulk_density": [1.23, 1, False]}), [2]),
    ],
)
def test_is_positive_not_zero_number_or_null_col(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.bulk_density
    test_function = DATAFRAME_DICT["is_positive_not_zero_number_or_null"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"tolerance": [1, None, -3]}), [2]),
        (pd.DataFrame({"tolerance": [1, np.NaN, -3]}), [2]),
        (pd.DataFrame({"tolerance": [1, None, "aaa"]}), [2]),
        (pd.DataFrame({"tolerance": [1, np.NaN, 3.3]}), [2]),
        (pd.DataFrame({"tolerance": [1, None, True]}), [2]),
    ],
)
def test_check_dataset_positive_int_or_Null_col(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.tolerance
    test_function = DATAFRAME_DICT["check_positive_int_or_Null"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"latitude": [-89.4, -90, -91.4]}), [2]),
        (pd.DataFrame({"latitude": [89, 90, 91]}), [2]),
        (pd.DataFrame({"latitude": [0, 90, None]}), [2]),
        (pd.DataFrame({"latitude": [0, 90, np.NaN]}), [2]),
        (pd.DataFrame({"latitude": [0, 90, False]}), [2]),
        (pd.DataFrame({"latitude": [0, 90, "alp_num"]}), [2]),
    ],
)
def test_is_valid_latitude_col(test_input_df: pd.DataFrame, test_invalid_array: list):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.latitude
    test_function = DATAFRAME_DICT["is_valid_latitude"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"longitude": [-179.4, -180.0, -181.4]}), [2]),
        (pd.DataFrame({"longitude": [179, 180, 181]}), [2]),
        (pd.DataFrame({"longitude": [0, 180, None]}), [2]),
        (pd.DataFrame({"longitude": [0, 180, np.NaN]}), [2]),
        (pd.DataFrame({"longitude": [0, 180, False]}), [2]),
        (pd.DataFrame({"longitude": [0, 180, "alp_num"]}), [2]),
    ],
)
def test_is_valid_longitude_col(test_input_df: pd.DataFrame, test_invalid_array: list):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.longitude
    test_function = DATAFRAME_DICT["is_valid_longitude"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"string_for_db": ["aaa", "_", "{"]}), [2]),
        (pd.DataFrame({"string_for_db": ["aaa", "b", "cc}"]}), [2]),
        (pd.DataFrame({"string_for_db": ["aaa", "bbb", "[cc"]}), [2]),
        (pd.DataFrame({"string_for_db": ["aaa", "bbb", "cc]"]}), [2]),
        (pd.DataFrame({"string_for_db": ["aaa", "bbb", "&cc"]}), [2]),
    ],
)
def test_check_string_available_for_database(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    from data_validation_module.src import DATAFRAME_DICT

    test_series = test_input_df.string_for_db
    test_function = DATAFRAME_DICT["check_string_available_for_database"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    logger.debug(type(invalid_list))
    logger.debug(f"test_invalid_array: {test_invalid_array}")
    logger.debug(f"invalid_list: {invalid_list}")
    assert test_invalid_array == invalid_list


def test_read_json_file(
    test_dataframe_config: dict, test_string_dataframe_config_json: str
):
    data_conf = read_json_file(test_string_dataframe_config_json)
    assert data_conf == test_dataframe_config


def test_iterate_data_config(
    test_df_name: str,
    test_dataframe_config: dict,
    test_df: pd.DataFrame,
    test_invalid_index_list: list,
):
    invalid_list = iterate_data_config(test_df_name, test_dataframe_config, test_df)
    logger.debug(invalid_list)
    logger.debug(test_invalid_index_list)
    diff = set(invalid_list) ^ set(test_invalid_index_list)
    assert not diff


# this tests doesn't function correctly


def test_split_invalid_data_row_0(
    test_invalid_df: pd.DataFrame,
    test_df_with_invalid_column_filled: pd.DataFrame,
    test_output_csv_dir: str,
):
    # 1. remove invalid_rows.csv
    data_dir = find_closest_filepath("data_validation_module/test_files")
    try:
        os.remove(data_dir / "invalid_rows.csv")
    except IOError:
        pass

    # 2. assert invalid_rows.csv
    split_invalid_data_rows(test_df_with_invalid_column_filled, test_output_csv_dir)
    df = pd.read_csv(data_dir / "invalid_rows.csv", index_col=0)
    assert df.shape == test_invalid_df.shape

    # 3. remove invalid_rows.csv
    os.remove(data_dir / "invalid_rows.csv")


def test_split_invalid_data_row_1(
    test_valid_df: pd.DataFrame,
    test_df_with_invalid_column_filled: pd.DataFrame,
    test_output_csv_dir: str,
):
    df = split_invalid_data_rows(
        test_df_with_invalid_column_filled, test_output_csv_dir
    )
    assert df.shape == test_valid_df.shape


def test_validate_column_depth_id(
    test_depth_id_column: pd.Series,
    test_invalid_list_depth_id: list,
    test_depth_id_function_name: str,
):
    invalid_list_index = validate_column(
        test_depth_id_function_name, test_depth_id_column
    )
    diff = set(invalid_list_index) ^ set(test_invalid_list_depth_id)
    assert not diff


def test_check_dataframe(
    test_df: pd.DataFrame,
    test_df_name: str,
    test_string_dataframe_config_json: str,
    test_output_csv_dir: str,
    test_valid_df: pd.DataFrame,
):
    df = check_dataframe(
        test_df_name, test_df, test_string_dataframe_config_json, test_output_csv_dir
    )
    # 1. assert
    assert df.shape == test_valid_df.shape

    # 2. remove invalid_rows.csv
    data_dir = find_closest_filepath("data_validation_module/test_files")
    os.remove(data_dir / "invalid_rows.csv")
