# Introduction

This folder contains all scripts used to generate the statistics out of a database as described below. There are many files and folders, and each will be explained in this readme.

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

First, make sure the relevant variables in `config.py` are set and are correct for your use case and database.

Next, the first step is to run `get_data.py`.

Now that you have the data, you can run `rq1.py`, `rq2_3_chisq.py` and `rq2_3_mannwhitney.py` as desired. Note that the final one takes a long time to run because there are many configurations to generate graphics for. Feel free to comment out the configurations you do not need for your own uses - just be aware that by default, everything runs.

*Note: Ensure you have software domains set up in your relevant dataset.*

## Results

The data gathered by `get_data.py` end up in a folder called `data`. The names of the files in this folder should be self-explanatory. The structure of a domain data file is as follows:
```
{
    "decision type": {
        "characteristic name":
            // if the characteristic is continuous
            [values: numerical data]
            // if the characteristic is categorical
            {
                "characteristic option": count of issues with this option for this characteristic: int
            }
    }
}
```

The results of these statistics scripts end up in the `results` folder. This folder has three subfolders after running the above scripts:

- `rq1`: which is where the data for RQ1 resides.
- `chisq`: which is where the chi-squared test results for RQ2 and RQ3 reside.
- `mannwhitney`: which is where the Mann-Whitney test results for RQ2 and RQ3 reside.

### RQ1

This folder does not hold many results. The `_single` `.csv`s use the simplified label system, while the `_multi` ones hold the intersected label system. The `.png`s are the Venn diagrams of the domain counts.

### Chi-Squared

For RQ2, each characteristic only has four files, and thus are not in their own folder: the regular and high-conf `.csv` and `.json` files.

For RQ3, due to each characteristic having many potential configurations, all results for one characteristic are in one folder, named for that characteristic. Within this folder, files are named like this: `<domain name>_<decision type mode: intersected or simple>[_high_conf]<.json or .csv>`. A chi-squared results .csv will hold several tables:

- `values`: the actual counts measured.
- `stats`: the chi-squared statistic from the test result.
- `pvals`: the p-values for this cell of the matrix.
- `expected`: what the chi-squared test expected in this cell, if all variables were independent
- `value/expected`: the ratio between given and expected value. This is the table that gets put into the thesis.

### Mann-Whitney

Every characteristic-RQ combination gets its own folder here. 

For RQ2, the files are as follows: the base of each set of images is `<characteristic name>[_fliers][_high_conf].csv`, so in total there are four potential bases. The base `.csv` holds the results from the Mann-Whitney test, with p-values. Each base then has a `<base name without the .csv>_plot[_arrows].png` associated with it, which is the visualisation of that base, with or without arrows, so in total two `.png`s per base. RQ2's visualisations are a group of boxplots.

For RQ3, the files are as follows: the base of each set of images is `<characteristic name>[_simple][_inverted or _full_only][_high_conf].csv`, similar to RQ2 but with more options:

- `_inverted`: means the plot's primary grouping is the domain, as opposed to non-inverted, whose primary grouping is the decision type.
- `_full_only`: means the plot does not contain domain-specific data: an attempt to declutter the graph, which was ultimately not used in the thesis, because the domain-specific data was deemed useful.

In total, there are therefore 12 `.csv`s. Here, too, every `.csv` has two `.png`s: `<base>_plot[_arrows].png`. Here, however, the plot is a grouped box plot: there is a primary grouping, labeled along the x-axis, and a secondary grouping, using colours described in the graph legend.

Also note that RQ3's results do not have a `_fliers` option. This is possible in the code, however, it was especially interesting for RQ2, therefore they were not generated for RQ3.

Apart from the generated results, the `mannwhitney` folder also has a script `collect.py` which gathers up all the results actually displayed in the thesis and copies them to the `forlatex` folder.

## Isolate Big Values and Big Value Identification

The `isolate_big_values.py` script is intended to generate a quick-and-dirty overview of values for three pain-point characteristics in your dataset. The results from it end up in the `data` folder as `values_counted{suffix}{[_archonly]}.json`, with `archonly` being a settable boolean in the script itself.

The regular result file (`values_counted.json`) has the following structure:
```
{
    "characteristic name": [
        [
            "characteristic option",
            [
                total issue count with this option: int,
                {
                    "domain name": issue count with this option in this domain: int
                }
            ]
        ]
    ]
}
```

The inverse files (`values_counted_inverse.json`) has the following structure:
```
{
    "domain name": {
        "characteristic name": {
            "characteristic option": issue count: int
        }
    }
}
```

The `jira_defaults` value count files only have the values defined as jira defaults, decluttering the data. This was the second attempted strategy for the three pain point characteristics but was ultimately not used.

### Big Value Identification

The `big_value_ident.py` script is a permutation of `isolate_big_values.py` which requires the result data from the above to work properly. It counts, per characteristic in `[issue_type, status, resolution]` (which are the three pain point characteristics due to their variability between Jira instances and projects, see the relevant Threats to Validity subsection in the thesis), per value of this characteristic, how many issues in this domain have this value for this characteristic. It generates the `values_ident_...` files in the same folder.

## Project-Specific Data

For the thesis, this data was categorised by software domain. However, it is also interesting to go by project, though not feasible in the thesis itself. Therefore, `get_data_projects.py` gets this data and `parse_data_projects.py` formats it into tables. There is a `projects` folder in both the `data` and `results` folder of this `statistics` folder to hold precisely this data. In `data`, each project has its own `_chars` and `_counts` files, with `_high_conf` variants as well. The `_chars` file holds the characteristics, with the same structure as the domain files, and the `_counts` file holds the plain amount of issues per decision type in that project. In the `results/projects` folder, there are three types of files:

- The `counts.csv`, `counts_percents.csv` and `_high_conf` variants: are simply the project's `_counts` files merged into a table format.
- The categorical characteristics: have the files `<charname>.csv`, `<charname>_percents.csv`, and `_high_conf` variants, which are exactly what they sound like.
- The continuous variables: have only the `<charname>.csv` and `_high_conf` variant, and hold the box-plot-relevant data for each project for that characteristic: mean, first and third quantiles, and standard deviation.

