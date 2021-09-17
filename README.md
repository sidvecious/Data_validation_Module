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

The steps of data harmonization and collection are performed in Seqana with two separate modules: the Soil Data Harmonization module and the module Upload To PosgreSQL.
The data validation module consists of a collection of functions for internal use by Seqana for automatic data validation.
The functions are called within the two main modules to check the consistency, integrity, usefulness, and accuracy of the dataset being harmonized and uploaded.
Seqana is a B2B start-up company specializing in satellite monitoring of soil organic carbon (SOC) for the voluntary carbon market.
To get good predictions of soil carbon content, the data in the database must be of high quality.
The data validation module is used to extend and unify data validation for the main modules.
The data structure to be analyzed as part of the data validation module is the DataFrame, a class in the Python library Pandas.
During validation, the following parameters are checked:
    1. data type in the rows of the DataFrame.
    2. semantic restriction of the data.

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
python -m pip install git+https://gitlab.com/cquest1/prototypes/data_validation_module@0.1.0
```


### Examples

- ADD SOME REPRESENTATIVE EXAMPLES HERE!

----


## TODO

1 - The architecture with dictionary must be replaced with a Class design
2 - Validation functions should be added for pandas Series
3 - Validation functions should be added for JSON file

----

## CHANGELOG

- ADD CHANGES HERE!

----

## Contact

Lorenzo Olivier ([lorenzo@cquest.ai](mailto:lorenzo@cquest.ai))
