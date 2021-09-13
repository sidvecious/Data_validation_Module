"""
This is not really part of the module, it is the orginal scratch,

that already work good, but only with two cases, i commit it for reference
"""
import json

import numpy as np
import pandas as pd
from file_path_tools.search_and_find import find_closest_filepath


def check_all(i, type_i):
    print(type(type_i))
    return type(i).__name__ == type_i


def check_none(i, _type_i):
    return not np.isnan(i)


DICT = {
    "check_positive_int": check_all,
    "check_date_format_YYYY_mm_dd": check_all,
    "check_none": check_none,
}


def initialize_json(dataframe_path: str):
    with open(find_closest_filepath(dataframe_path)) as dfj:
        data_config = json.load(dfj)
    return data_config


def split_invalid_data_rows(df):
    data_dir = find_closest_filepath("data_validation_module/test_files")
    df[df.invalid_data == 1].to_csv(data_dir / "invalid_rows.csv")
    return df[df.invalid_data == 0]


def main(df_name, df, config_path):
    data_config = initialize_json(config_path)
    invalid_list = iterate_data_config(df_name, df, data_config)
    valid_data = 0
    if "invalid_data" not in df:
        df["invalid_data"] = valid_data
    invalid_data = 1
    df.loc[invalid_list, "invalid_data"] = invalid_data
    return split_invalid_data_rows(df)


def iterate_column(series, mapped_function, type_series):
    print(f"mapped_function:{mapped_function}")
    invalid_list = np.unique(
        np.where(series.apply(lambda x: not mapped_function(x, type_series)))
    )
    return invalid_list


def iterate_data_config(df_name, df, data_config):
    invalid_list = []
    if df_name in data_config:
        df_config = data_config[df_name]
        for row in df_config["rows"]:
            type_series = row["type"]
            print(f"type_series is type: {type(type_series)}")
            series = df[row["name"]]
            if type(row["harmony"]) is not list:
                print("sorry i don't understand you")
                continue
            for fnname in row["harmony"]:
                invalid_list.extend(
                    harmonize_column(df_name, fnname, series, type_series)
                )
                invalid_list = list(set(invalid_list))
    return invalid_list


def harmonize_column(df_name, fnname, series, type_series):
    if fnname in DICT:
        mapped_function = DICT[fnname]
        return iterate_column(series, mapped_function, type_series)
    else:
        print(f"warning: unable to find {fnname} for {df_name}")
        return []


data = {"date_id": ["a", "b", "c", None, "f"], "geom_id": [6.0, 12, 18, 24, None]}
df = pd.DataFrame(data)
# print(iterate_data_config("sample_gdf", df, config))
print(main("sample_gdf", df, "dataframe_config.json"))
