# CCC Runner

A CLI tool to easily verify CCC answers by running test cases programatically.

## Install

Install the prerequisites by running `python3 -m pip install -r requirements.txt`.

A virtual environment is recommended but not necessary.

## Usage

Run the `app.py` file with python, eg. `python3 app.py`.

Alternatively, the `runner.py` file can be used if you prefer the CLI:

`python3 runner.py <PATH TO TEST DATA> <COMMAND TO LAUNCH PROGRAM>`.

Regardless of the way you choose, the path to the test data should point to the
extracted solutions tarball downloaded from the CCC website.

The command is how your program would be run from the command line, eg. `python3 j1_solution.py`.

