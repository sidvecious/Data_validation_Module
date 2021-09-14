import pandas as pd
from data_validation_module.data_validation_module.src import (
    check_dataframe,
    validate_column,
    iterate_column,
    iterate_data_config,
    read_json_file,
    split_invalid_data_rows,
)
from loguru import logger


# test of iterate_column with the depth_id column
def test_check_dataset_depth_id_col_0(
    test_depth_id_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_list_depth_id: list,
):
    result = iterate_column(
        test_depth_id_column, test_mapped_function["depth_id"], "str"
    )
    logger.debug(result)
    assert result == test_invalid_list_depth_id


# test of iterate column with date_id column
def test_check_date_id_col_0(
    test_date_id_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_list_date_id: list,
):
    result = iterate_column(test_date_id_column, test_mapped_function["date_id"], "str")
    logger.debug(result)
    assert result == test_invalid_list_date_id


# test of iterate column with a string column
def test_check_soil_texture_col_0(
    test_soil_texture_column: pd.Series,
    test_mapped_function: dict,
    test_invalid_soil_texture: list,
):
    result = iterate_column(
        test_soil_texture_column, test_mapped_function["soil_texture"], "str"
    )
    logger.debug(result)
    assert result == test_invalid_soil_texture


def test_read_json_file(
    test_dataframe_config: dict, test_string_dataframe_config_json: str
):
    data_conf = read_json_file(test_string_dataframe_config_json)
    assert data_conf == test_dataframe_config


def test_iterate_data_config(
    test_df_name: str,
    test_dataframe_config: dict,
    test_df: pd.DataFrame,
    test_invalid_list: list,
):
    invalid_list = iterate_data_config(test_df_name, test_dataframe_config, test_df)
    assert all(a == b for a, b in zip(invalid_list, test_invalid_list))


# this tests doesn't function correctly
"""
def test_split_invalid_data_row_0(test_invalid_df, test_df_with_invalid_column_filled):
    # 1. remove invalid_rows.csv
    data_dir = find_closest_filepath("data_validation_module/test_files")
    try:
        os.remove(data_dir / "invalid_rows.csv")
    except IOError:
        pass

    # 2. assert invalid_rows.csv
    split_invalid_data_rows(test_df_with_invalid_column_filled)
    df = pd.read_csv(data_dir / "invalid_rows.csv")
    assert df.shape == test_invalid_df.shape

    # 3. remove invalid_rows.csv
    os.remove(data_dir / "invalid_rows.csv")



def test_split_invalid_data_row_1(test_valid_df, test_df_with_invalid_column_filled):
    df = split_invalid_data_rows(test_df_with_invalid_column_filled)
    assert df.shape == test_valid_df.shape


def test_check_dataframe(
        test_df,
        test_df_name,
        test_valid_df,
        test_string_dataframe_config_json,
        test_string_dataframe_type_json
):
    df = check_dataframe(
        test_df_name,
        test_df,
        test_string_dataframe_config_json
    )
    assert df.shape == test_valid_df.shape

# validate_column need to be tested
def test_validate_column():
    pass


    """
