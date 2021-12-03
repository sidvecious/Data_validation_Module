![pipeline](https://gitlab.com/cquest1/prototypes/data_validation_module/badges/master/pipeline.svg)
![coverage](https://gitlab.com/cquest1/prototypes/data_validation_module/badges/master/coverage.svg)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg "black")](https://github.com/python/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


# Data_validation_module

A tool with different functions for the data validation

- [Description](#description)
- [Development](#development)
- [Usage](#usage)
- [TODO](#todo)
- [CHANGELOG](#changelog)
- [Contact](#contact)

----

## Description

The steps of data harmonization and collection are performed in Seqana with two separate modules: 
the Soil Data Harmonization module and the module Upload To PosgreSQL.
The data validation module consists of a collection of functions for internal use by Seqana for automatic data 
validation.
The functions are called within the two main modules to check the consistency, integrity, usefulness, 
and accuracy of the dataset being harmonized and uploaded.
Seqana is a B2B start-up company specializing in satellite monitoring of soil organic carbon (SOC) for the voluntary 
carbon market.
To get good predictions of soil carbon content, the data in the database must be of high quality.
The data validation module is used to extend and unify data validation for the main modules.
The data structures to be analyzed as part of the data validation module are:

1. The DataFrame, a two-dimensional tabular data structure in the Python library Pandas 
During validation, the following parameters are checked:
    A. consistency of the Series names with the configuration json file
    B. data type in the rows of the DataFrame.
    C. semantic restriction of the data.
Dataframe configuration file: 
Several dataframes can be encoded in the json configuration file, 
each dataframe has a list of columns to validate, 
for each column there is one or more validations.

2. The Dictionary, an unordered mutable Python container with a key-values pairs
During validation, the following parameters are checked:
    A. consistency of the keys with the configuration json file 
    B. data Type of the values
    C. semantic restriction of the values
Dictionary configuration file:
Several dictionaries can be encoded in the json configuration file, 
The validation of each dictionary is composed of a 3-level nested structure AND, OR, AND. 
   - for each dictionary there are one or more constraints, the dictionary is valid if all the constraints are valid
   - for each Constraint there are one or more rules, the Constraint is valid if at least one rule is true.
   - for each rule there are one or more key-value pairs of the dictionary to validate, 
   the rule is valid if all the key-value pairs inside this rule are valid.  
Note that the same key-value pair of the dictionary can belong to different rules because 
in the Soil_data_harmonization dictionary, it is possible to have different combinations of non-zero values to get 
a valid dictionary.

----

## Development

1. Write some code.
2. Write a test.
3. Check whether tests run locally with ```pytest --cov --cov-report html```,
   to check the coverage report at htmlcov/index.html
4. If all tests run, commit and push to git.
5. Wait for gitlab-CI to return green light - all tests pass, if not check error report and fix bugs, return to step 1.
6. Update CHANGELOG in README
7. Bump version in setup.py: +0.0.1 for minor updates/refactor, +0.1.0 for breaking changes, major refactor
8. ```git commit README.md setup.py```
9. ```git tag <new_version_number>```
10. ```git push origin <new_version_number>```
- Regularly update the requirements.txt file for ci/cd purposes

- Use the created conda environment for development
- Regularly update the requirements.txt file for ci/cd purposes


----

## Usage

### Cloning This Repo

```bash
git clone --recurse-submodules https://www.gitlab.com/cquest1/prototypes/data_validation_module.git
```

### Installing the python package

```bash
python -m pip install git+https://gitlab.com/cquest1/prototypes/data_validation_module@0.1.11
```


### Examples

- ADD SOME REPRESENTATIVE EXAMPLES HERE!

----


## TODO
1 - Test validation of dictionaries in production
2 - Validation functions should be added for JSON file
3 - Validation functions should be added for pandas Series
4 - The architecture with dictionary must be replaced with a Class design



----

## CHANGELOG

- ADD CHANGES HERE!

----

## Contact

Lorenzo Olivier ([lorenzo@cquest.ai](mailto:lorenzo@cquest.ai))
