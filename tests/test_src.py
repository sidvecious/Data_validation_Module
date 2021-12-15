import json
import os
from pathlib import Path, PosixPath

import numpy as np
import pandas as pd
import pytest
from loguru import logger

from data_validation_module.__main__ import (
    TYPES_IN_DICTIONARY_VALUES,
    VALIDATION_DICT,
    check_dataframe,
    check_dictionary,
    check_json_file,
    find_invalid_data_indices,
    find_invalid_dict_values,
    iterate_data_config,
    iterate_dict_constraint,
    iterate_dict_rule,
    iterate_dict_validation,
    iterate_dictionary_config,
    print_invalid_dictionary,
    read_json_file,
    split_invalid_data_rows,
    validate_column,
    validate_functions_for_dictionaries,
)


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
        (pd.DataFrame({"soc_percent": [103, None, 3.3]}), [0]),
        (pd.DataFrame({"soc_percent": [np.NaN, 103, 3.3]}), [1]),
        (pd.DataFrame({"soc_percent": ["string", 2.2, 3.3]}), [0]),
        (pd.DataFrame({"soc_percent": [True, 1.1, 2.2]}), [0]),
    ],
)
def test_is_valid_percent_value_col(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    test_series = test_input_df.soc_percent
    test_function = VALIDATION_DICT["is_valid_percent_value_or_null"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    assert test_invalid_array == invalid_list


@pytest.mark.parametrize(
    "test_input_df, test_invalid_array",
    [
        (pd.DataFrame({"soc_percent": [0.1, 0.2, 103.3]}), [2]),
        (pd.DataFrame({"soc_percent": [1, 0.2, -2.3]}), [2]),
        (pd.DataFrame({"soc_percent": [103, None, 0.3]}), [0]),
        (pd.DataFrame({"soc_percent": [np.NaN, 103, 0.3]}), [1]),
        (pd.DataFrame({"soc_percent": ["string", 0.2, 0.3]}), [0]),
        (pd.DataFrame({"soc_percent": [True, 0.1, 0.2]}), [0]),
    ],
)
def test_is_valid_ratio_value_col(
    test_input_df: pd.DataFrame, test_invalid_array: list
):
    test_series = test_input_df.soc_percent
    test_function = VALIDATION_DICT["is_valid_ratio_value_or_null"]
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

    test_series = test_input_df.db_id
    test_function = VALIDATION_DICT["check_positive_int"]
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

    test_series = test_input_df.bulk_density
    test_function = VALIDATION_DICT["is_greater_zero_or_null"]
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

    test_series = test_input_df.tolerance
    test_function = VALIDATION_DICT["check_positive_int_or_Null"]
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

    test_series = test_input_df.latitude
    test_function = VALIDATION_DICT["is_valid_latitude"]
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

    test_series = test_input_df.longitude
    test_function = VALIDATION_DICT["is_valid_longitude"]
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

    test_series = test_input_df.string_for_db
    test_function = VALIDATION_DICT["check_string_available_for_database"]
    invalid_list = find_invalid_data_indices(test_series, test_function)
    logger.debug(type(invalid_list))
    logger.debug(f"test_invalid_array: {test_invalid_array}")
    logger.debug(f"invalid_list: {invalid_list}")
    assert test_invalid_array == invalid_list


def test_read_json_file(test_dataframe_config: dict, test_dataframe_config_path: Path):
    data_conf = read_json_file(test_dataframe_config_path)
    assert data_conf == test_dataframe_config


def test_iterate_data_config(
    test_df_name: str,
    test_dataframe_config: dict,
    test_df: pd.DataFrame,
    test_invalid_index_list: list,
):
    invalid_list = iterate_data_config(test_df_name, test_dataframe_config, test_df)
    diff = set(invalid_list) ^ set(test_invalid_index_list)
    assert not diff


def test_split_invalid_data_row_0(
    test_invalid_df: pd.DataFrame,
    test_df_with_invalid_column_filled: pd.DataFrame,
    test_output_dir: Path,
):
    # 1. remove invalid_rows.csv
    try:
        os.remove(test_output_dir / "invalid_rows.csv")
    except IOError:
        pass

    # 2. assert invalid_rows.csv
    split_invalid_data_rows(test_df_with_invalid_column_filled, test_output_dir)
    df = pd.read_csv(test_output_dir / "invalid_rows.csv", index_col=0)
    assert df.shape == test_invalid_df.shape

    # 3. remove invalid_rows.csv
    os.remove(test_output_dir / "invalid_rows.csv")


def test_split_invalid_data_row_1(
    test_valid_df: pd.DataFrame,
    test_df_with_invalid_column_filled: pd.DataFrame,
    test_output_dir: Path,
):
    df = split_invalid_data_rows(test_df_with_invalid_column_filled, test_output_dir)
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
    test_dataframe_config_path: Path,
    test_output_dir: Path,
    test_valid_df: pd.DataFrame,
):
    df = check_dataframe(
        test_df_name, test_df, test_dataframe_config_path, test_output_dir
    )

    # 1. assert
    assert df.shape == test_valid_df.shape

    # 2. remove invalid_rows.csv
    os.remove(test_output_dir / "invalid_rows.csv")


@pytest.mark.parametrize(
    "test_table_name, test_mapped_function, test_target_value, test_result",
    [
        ("database_id", "check_int_greater_zero", 1, []),
        ("database_id", "check_int_greater_zero", 0, ["database_id"]),
        ("database_id", "check_int_greater_zero", -1, ["database_id"]),
        ("database_id", "check_int_greater_zero", 12.34, ["database_id"]),
        ("db_string", "check_string_available_for_database", "abc_123", []),
        ("db_string", "check_string_available_for_database", "abc*123", ["db_string"]),
        ("db_string", "check_string_available_for_database", "!@#$%^&*", ["db_string"]),
        ("db_string", "check_string_available_for_database", None, ["db_string"]),
        ("dir_path", "is_valid_dir_path", PosixPath("test_files"), []),
        ("dir_path", "is_valid_dir_path", Path("test_files"), []),
        ("dir_path", "is_valid_dir_path", PosixPath("foo/foo"), ["dir_path"]),
        (
            "dir_path",
            "is_valid_dir_path",
            Path("test_files/test_json.json"),
            ["dir_path"],
        ),
        ("file_path", "is_valid_file_path", Path("test_files/test_json.json"), []),
        ("file_path", "is_valid_file_path", Path("test_files/test_txt.txt"), []),
        (
            "file_path",
            "is_valid_file_path",
            Path("test_files/test_json.foo"),
            ["file_path"],
        ),
        ("file_path", "is_valid_file_path", Path("test_files"), ["file_path"]),
        ("json_file", "is_string_represent_json", "foo/foo.json", []),
        ("json_file", "is_string_represent_json", "foo.json/", ["json_file"]),
        ("json_file", "is_string_represent_json", "foo++.json", ["json_file"]),
        ("json_file", "is_string_represent_json", "foo/foo.txt", ["json_file"]),
    ],
)
def test_find_invalid_dict_values(
    test_table_name: str,
    test_mapped_function: str,
    test_target_value: TYPES_IN_DICTIONARY_VALUES,
    test_result: list,
):
    test_function = VALIDATION_DICT[test_mapped_function]
    list_result = find_invalid_dict_values(
        test_table_name, test_function, test_target_value
    )
    assert list_result == test_result


def test_iterate_dict_validation_right(
    test_table_validation_database_id_test_rule_or_1: dict,
    test_target_dict_right: dict,
    test_rule_database_id_test_rule_or_1: list
    # test_rule_database_id_test_rule_or_1 added for json
):
    test_list = []
    test_result = iterate_dict_validation(
        test_table_validation_database_id_test_rule_or_1,
        test_target_dict_right,
        test_list,
        test_rule_database_id_test_rule_or_1,
    )
    result_list = []
    assert test_result == result_list


def test_iterate_nested_dict_validation_right(
    test_table_validation_nested_db_table_name_1: dict,
    test_target_nested_dict_right: dict,
    test_rule_nested_unique_rule_1: list,
):
    test_list = []
    test_result = iterate_dict_validation(
        test_table_validation_nested_db_table_name_1,
        test_target_nested_dict_right,
        test_list,
        test_rule_nested_unique_rule_1,
    )
    result_list = []
    assert test_result == result_list


def test_iterate_nested_dict_validation_wrong_db_table_name(
    test_table_validation_nested_db_table_name_1: dict,
    test_target_nested_dict_wrong_db_table_name: dict,
    test_rule_nested_unique_rule_1: list,
):
    test_list = []
    test_result = iterate_dict_validation(
        test_table_validation_nested_db_table_name_1,
        test_target_nested_dict_wrong_db_table_name,
        test_list,
        test_rule_nested_unique_rule_1,
    )
    result_list = ["db_table_name"]
    assert test_result == result_list


def test_iterate_nested_dict_validation_number_wrong(
    test_table_validation_nested_number_1: dict,
    test_target_nested_dict_two_tables_wrong: dict,
    test_rule_nested_unique_rule_1: list,
):
    test_list = []
    test_result = iterate_dict_validation(
        test_table_validation_nested_number_1,
        test_target_nested_dict_two_tables_wrong,
        test_list,
        test_rule_nested_unique_rule_1,
    )
    result_list = ["number"]
    assert test_result == result_list


def test_iterate_dict_validation_wrong_key(
    test_table_validation_database_id_test_rule_or_1: dict,
    test_target_dict_wrong_key: dict,
    test_rule_database_id_test_rule_or_1: list
    # test_rule_database_id_test_rule_or_1 added for json
):
    test_list = []
    with pytest.raises(SystemExit) as ext:
        iterate_dict_validation(
            test_table_validation_database_id_test_rule_or_1,
            test_target_dict_wrong_key,
            test_list,
            test_rule_database_id_test_rule_or_1,
        )
        assert ext.type == SystemExit


def test_iterate_dict_rule_right1(
    test_rule_database_id_test_rule_or_1: list,
    test_target_dict_right,
):
    test_invalid_rule_report = ""
    at_least_a_rule_is_working, invalid_rule_report = iterate_dict_rule(
        test_rule_database_id_test_rule_or_1,
        test_target_dict_right,
        test_invalid_rule_report,
    )
    assert invalid_rule_report == ""


def test_iterate_dict_rule_right2(
    test_rule_database_id_test_rule_or_1: list,
    test_target_dict_right: dict,
):
    test_invalid_rule_report = ""
    at_least_a_rule_is_working, invalid_rule_report = iterate_dict_rule(
        test_rule_database_id_test_rule_or_1,
        test_target_dict_right,
        test_invalid_rule_report,
    )
    assert at_least_a_rule_is_working


def test_iterate_dict_rule_wrong_database_id_1(
    test_rule_database_id_test_rule_or_1: list,
    test_target_dict_wrong_database_id: dict,
    test_invalid_rule_report_test_rule_or_1: str,
):
    test_invalid_rule_report = ""
    at_least_a_rule_is_working, invalid_rule_report = iterate_dict_rule(
        test_rule_database_id_test_rule_or_1,
        test_target_dict_wrong_database_id,
        test_invalid_rule_report,
    )
    assert invalid_rule_report == test_invalid_rule_report_test_rule_or_1


def test_iterate_dict_rule_wrong_database_id_2(
    test_rule_database_id_test_rule_or_1: list,
    test_target_dict_wrong_database_id: dict,
):
    test_invalid_rule_report = ""
    at_least_a_rule_is_working, invalid_rule_report = iterate_dict_rule(
        test_rule_database_id_test_rule_or_1,
        test_target_dict_wrong_database_id,
        test_invalid_rule_report,
    )
    assert at_least_a_rule_is_working is False


def test_iterate_dict_constraint_right_1(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_right: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_right,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert invalid_dataset_report == ""


def test_iterate_dict_constraint_right_2(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_right: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_right,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert no_constraint_failed


def test_iterate_dict_constraint_wrong_database_id_1(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_wrong_database_id: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_wrong_database_id,
        invalid_dataset_report,
        no_constraint_failed,
    )
    result_string = ""
    assert invalid_dataset_report == result_string


def test_iterate_dict_constraint_wrong_database_id_2(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_wrong_database_id: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_wrong_database_id,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert no_constraint_failed


def test_iterate_dict_constraint_wrong_db_id_and_string1(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_wrong_db_id_and_string: dict,
    test_invalid_rule_report_both_rules_broken: str,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_wrong_db_id_and_string,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert invalid_dataset_report == test_invalid_rule_report_both_rules_broken


def test_iterate_dict_constraint_wrong_db_id_and_string2(
    test_constraint_test_constraint_or_1: dict,
    test_target_dict_wrong_db_id_and_string: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_test_constraint_or_1,
        test_target_dict_wrong_db_id_and_string,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert not no_constraint_failed


def test_iterate_nested_dict_constraint_right_1(
    test_constraint_nested_double_layer_1: dict,
    test_target_nested_dict_right: dict,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_nested_double_layer_1,
        test_target_nested_dict_right,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert invalid_dataset_report == ""


def test_iterate_nested_dict_constraint_wrong_1(
    test_constraint_nested_double_layer_1: dict,
    test_target_nested_dict_wrong_db_table_name: dict,
    test_invalid_nested_dictionary_constraint_failed: str,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_nested_double_layer_1,
        test_target_nested_dict_wrong_db_table_name,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert invalid_dataset_report == test_invalid_nested_dictionary_constraint_failed


def test_iterate_nested_dict_constraint_wrong_2(
    test_constraint_nested_double_layer_1: dict,
    test_target_nested_dict_two_tables_wrong: dict,
    test_invalid_nested_dictionary_constraint_failed_two_times: str,
):
    invalid_dataset_report = ""
    no_constraint_failed = True
    invalid_dataset_report, no_constraint_failed = iterate_dict_constraint(
        test_constraint_nested_double_layer_1,
        test_target_nested_dict_two_tables_wrong,
        invalid_dataset_report,
        no_constraint_failed,
    )
    assert (
        invalid_dataset_report
        == test_invalid_nested_dictionary_constraint_failed_two_times
    )


@pytest.mark.parametrize(
    "test_table_name, test_fn_name, test_target_value, test_result",
    [
        ("database_id", "check_int_greater_zero", 1, []),
        ("database_id", "not_existing_function", 1, ["database_id"]),
    ],
)
def test_validate_functions_for_dictionaries(
    test_table_name: str,
    test_fn_name: str,
    test_target_value: TYPES_IN_DICTIONARY_VALUES,
    test_result: list,
):
    list_result = validate_functions_for_dictionaries(
        test_table_name, test_fn_name, test_target_value
    )
    assert list_result == test_result


@pytest.mark.parametrize(
    "test_invalid_dataset_report, test_result",
    [("print_test_1, print_test_2", "print_test_1, print_test_2"), ("", "")],
)
def test_print_invalid_dictionary(
    test_invalid_dataset_report: str,
    test_result: str,
    test_invalid_dictionary_name: str,
):
    # 1. remove invalid_dictionaries.txt
    test_output_dir = Path("test_files")
    try:
        os.remove(test_output_dir / test_invalid_dictionary_name)
    except IOError:
        pass

    # 2. assert invalid_dictionaries.txt contents == test_result
    print_invalid_dictionary(
        test_invalid_dataset_report, test_output_dir, test_invalid_dictionary_name
    )
    test_complete_path = test_output_dir / test_invalid_dictionary_name
    with open(test_complete_path) as f:
        file_contents = " ".join(line.strip() for line in f)

    assert file_contents == test_result

    # 3. remove invalid_dictionaries.txt
    os.remove(test_output_dir / test_invalid_dictionary_name)


def test_iterate_dictionary_config_right_dict_1(
    test_target_dict_right: dict, test_dict_name_1: str, test_config_dictionary: dict
):
    result_invalid_report = iterate_dictionary_config(
        test_target_dict_right, test_dict_name_1, test_config_dictionary
    )
    assert result_invalid_report == ""


def test_iterate_dictionary_config_right_dict_2(
    test_target_dict_right: dict, test_dict_name_2: str, test_config_dictionary: dict
):
    result_invalid_report = iterate_dictionary_config(
        test_target_dict_right, test_dict_name_2, test_config_dictionary
    )
    assert result_invalid_report == ""


def test_iterate_dictionary_config_wrong_database_id_dict_1(
    test_target_dict_wrong_database_id: dict,
    test_dict_name_1: str,
    test_config_dictionary: dict,
    test_invalid_dictionary_single_rule_failed: str,
):
    test_invalid_report = iterate_dictionary_config(
        test_target_dict_wrong_database_id, test_dict_name_1, test_config_dictionary
    )
    assert test_invalid_dictionary_single_rule_failed == test_invalid_report


def test_iterate_dictionary_config_wrong_database_id_dict_2(
    test_target_dict_wrong_database_id: dict,
    test_dict_name_2: str,
    test_config_dictionary: dict,
):
    test_invalid_report = iterate_dictionary_config(
        test_target_dict_wrong_database_id, test_dict_name_2, test_config_dictionary
    )
    result_invalid_report = ""
    assert result_invalid_report == test_invalid_report


def test_iterate_dictionary_config_wrong_db_id_and_string_dict_2(
    test_target_dict_wrong_db_id_and_string: dict,
    test_dict_name_2: str,
    test_config_dictionary: dict,
    test_invalid_dictionary_both_rules_failed: str,
):
    test_invalid_report = iterate_dictionary_config(
        test_target_dict_wrong_db_id_and_string,
        test_dict_name_2,
        test_config_dictionary,
    )
    assert test_invalid_report == test_invalid_dictionary_both_rules_failed


def test_check_dictionary_right(
    test_target_dict_right: dict,
    test_dict_name_2: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
):
    validate_dict = check_dictionary(
        test_target_dict_right,
        test_dict_name_2,
        test_dictionary_config_path,
        test_output_dir,
    )
    assert validate_dict == test_target_dict_right


def test_check_dictionary_wrong_values_dict_2(
    test_target_dict_wrong_db_id_and_string: dict,
    test_dict_name_2: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
):
    invalid_dictionary = "invalid_dictionaries.txt"
    # 1. remove invalid_dictionaries.txt
    try:
        os.remove(test_output_dir / invalid_dictionary)
    except FileNotFoundError:
        pass

    # 2. call check_dictionary
    check_dictionary(
        test_target_dict_wrong_db_id_and_string,
        test_dict_name_2,
        test_dictionary_config_path,
        test_output_dir,
    )

    # 3. assert
    result = "test_target_dict_2 is Invalid: The Constraint test_constraint_or is not valid, because all the rules fails: Invalid rule test_rule_or_1: for validations ['database_id'] Invalid rule test_rule_or_2: for validations ['db_string']"
    test_complete_path = test_output_dir / invalid_dictionary
    with open(test_complete_path, "r") as f:
        file_contents = " ".join(line.strip() for line in f)

    assert file_contents == result

    # 4. remove invalid_dictionaries.txt
    os.remove(test_output_dir / invalid_dictionary)


def test_check_dictionary_with_wrong_key_dict_1(
    test_target_dict_wrong_key: dict,
    test_dict_name_1: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
):
    with pytest.raises(SystemExit) as ext:
        check_dictionary(
            test_target_dict_wrong_key,
            test_dict_name_1,
            test_dictionary_config_path,
            test_output_dir,
        )
        assert ext.type == SystemExit


def test_check_target_json_right(
    test_target_json_path: Path,
    test_nested_dict_name_1: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
):
    validate_dict = check_json_file(
        test_target_json_path,
        test_nested_dict_name_1,
        test_dictionary_config_path,
        test_output_dir,
    )
    assert validate_dict == test_target_json_path


def test_check_target_json_wrong_values_1(
    test_temporary_json_config_path: Path,
    test_nested_dict_name_1: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
    test_target_nested_dict_two_tables_wrong: dict,
):
    invalid_json = "invalid_json.txt"
    # 1. remove invalid_json.txt and test_temporary_json_config
    try:
        os.remove(test_output_dir / invalid_json)
    except FileNotFoundError:
        pass
    try:
        os.remove(test_temporary_json_config_path)
    except FileNotFoundError:
        pass

    # 2. create wrong json_file
    with open(test_temporary_json_config_path, "w") as outfile:
        json.dump(test_target_nested_dict_two_tables_wrong, outfile)

    # 3. call check_json_file
    check_json_file(
        test_temporary_json_config_path,
        test_nested_dict_name_1,
        test_dictionary_config_path,
        test_output_dir,
    )

    # 4. assert
    result = "test_target_nested_dict_1 is Invalid: The Constraint double_layer is not valid, because all the rules fails: Invalid rule unique_rule: for validations ['db_table_name', 'number']"
    test_complete_path = test_output_dir / invalid_json
    with open(test_complete_path, "r") as f:
        file_contents = " ".join(line.strip() for line in f)

    assert file_contents == result

    # 5. remove invalid_json.txt and test_temporary_json_config.json
    os.remove(test_output_dir / invalid_json)
    os.remove(test_temporary_json_config_path)


def test_check_wrong_dictionary_or_json_name(
    test_target_json_path: Path,
    test_wrong_dict_name: str,
    test_dictionary_config_path: Path,
    test_output_dir: Path,
):
    invalid_json = "invalid_json.txt"
    # 1. remove invalid_json.txt
    try:
        os.remove(test_output_dir / invalid_json)
    except FileNotFoundError:
        pass

    # 2. call check_json_file
    check_json_file(
        test_target_json_path,
        test_wrong_dict_name,
        test_dictionary_config_path,
        test_output_dir,
    )

    # 3. assert
    result = f"The name '{test_wrong_dict_name}' is not in the json configuration file!"
    test_complete_path = test_output_dir / invalid_json
    with open(test_complete_path, "r") as f:
        file_contents = " ".join(line.strip() for line in f)

    assert file_contents == result

    # 4. remove invalid_json.txt and test_temporary_json_config.json
    os.remove(test_output_dir / invalid_json)
