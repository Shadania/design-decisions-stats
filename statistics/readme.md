# Introduction

# Setup

The Python version used for this project is Python 3.10.0.

Run `pip install -r requirements.txt` to install the listed requirements.
Then, run `python setup.py` to ensure you have the required setup.

## Local Database - Setup

If you want to use local data, you need to set up the required database and Docker API first.

- Make sure you have Docker installed.
- Download and run the [relevant GitHub repository](https://github.com/mining-design-decisions/maestro-issues-db) to get the Docker container up and running (see the readme).
- Load up your container with data (see the readme also).
- Set the `config.py` variables to the correct values.
- Ensure you have the statistics ready (call `POST /statistics/calculate` endpoint, which takes a while depending on your dataset size)

# Usage

First, make sure the relevant variables in `config.py` are set and are correct: `model`, `db_url` and `keep_format`.

Next, the first step is to run `get_data.py`.

Now that you have the data, you can run `rq1.py`, `rq2_3_chisq.py` and `rq2_3_mannwhitney.py` as desired. Note that the final one takes a long time to run because there are many configurations to generate graphics for.

*Note: Ensure you have software domains set up in your relevant dataset.*

## Isolate Big Values

The `isolate_big_values.py` script is intended to generate a quick-and-dirty overview of values for three pain-point characteristics in your dataset. The results from it end up in the `data` folder as `values_counted{suffix}.json`.

# Folders of Data

*Note: `name` here refers to either empty-string for normal dataset or `_high_conf` for the exclusively high-confidence dataset*

- `data`: the data resulting from `get_data.py`. Format is `counts{name}.json`, `domain_{dom}{name}.json`
- `results/rq1`: Contains results for RQ1 in both json and csv format.
- `results/chisq/`: Contains results for RQ2 and RQ3 from the chi-squared test, for RQ3 in folders per characteristic that are named `rq3_{characteristic name}`.
- `results/mannwhitney/`: Contains results for RQ2 and RQ3 from the chi-squared test, in folders per characteristic that are named `rq{2 or 3}_{characteristic name}`.