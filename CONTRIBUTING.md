# CONTRIBUTING

## Guidelines
- fork the project
- clone the forked project
- pip install the nepali_date in editable mode. On the root directory of project do `$ pip install -e .`
- install `pytest` for running tests. ```$ pip install pytest```
- install `flake8` for code formatting check. ```$ pip install flake8```
- check if all tests are passed by ```$ pytest```
- start contributing
- before pushing the changes check again if the tests are passed ```$ pytest```
- also check code formatting has any issues `$ flake8 nepali_datetime --max-line-length=120`
- push your code and raise the PR to `develop` branch

**Note: If you're confused on what to contribute in for, you can search for *TODO's* in the code & pick up which ever
you're comfortable with.**


## Preparing a new release
- Checkout out from the `main` branch with the name of branch of the version like `v1.0.8.3`.
- Update the release version in the `nepali_datetime/__init__.py` file name by updating the variable `__version__`.
- Update the documentation to reflect the release version by rebuilding the documentation inside `docs/` using the command `make html`. Make sure you install all the documentation dependecies before rebuilding it, which is in `docs/requirements.txt`.


#### *** HAPPY CONTRIBUTING ! ***
