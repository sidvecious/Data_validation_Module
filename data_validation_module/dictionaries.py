from data_validation_module.data_validation_module.src import (  # check_double_90,; check_double_180,; check_positive_int,; check_positive_int_or_Null,; check_range_from_zero_to_hundred,; check_string_available_for_database,
    check_date_format_YYYY_mm_dd,
    check_string_format_nnn_mmm,
    check_type_of_row,
)

# this dictionary must record all columns to be checked
# and their validation functions
# OPEN QUESTION 3:
# for the moment iterate_column is tested only for this functions
DATAFRAME_DICT = {
    "date_id": check_date_format_YYYY_mm_dd,
    "depth_id": check_string_format_nnn_mmm,
    "soil_texture": check_type_of_row,
}
