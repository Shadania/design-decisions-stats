# Introduction

This folder contains all helper scripts used to beautify and gather result graphics and tables for the thesis. All subsections of this readme describe a folder or file.

## `to_latex.py`, `input.txt`, `output.tex`, folder `oldinputs`

This script converts regular `.csv` tables into the LaTeX format used in the thesis document. Paste the `.csv` textual data into the `input.txt` file, run the `to_latex.py` script, and the result will be in `output.tex`.

There are no dependencies for this script except to have the same Python version (3.10) installed as the main statistics scripts.

The script will expect the same design decision names (existence, executive, property, and combinations) and domain names as the thesis uses.

This script is used for the tables relating to Chi-Squared test results for all RQs.

### Usage

#### RQ1

For tables from RQ1, copy-paste the `value/expected` set from the `.csv` into `input.txt`. Add `domain` at the start of the first line (before the first comma), and `non-arch` at the end of the first line (after the last comma) (if it's not there yet, and if it is but in a different format, best to correct it to this for consistency) (do not add a new comma, a comma with nothing after it in the line will add an empty column). Run the script. Paste the result into LaTeX as-is. Enjoy your table.

#### RQ2

For tables from RQ2, copy-paste the `value/expected` set from the `.csv` into `input.txt`. Add `domain` at the start of the first line (before the comma). Run the script.

Alternatively, use the `rq2.py` script to run everything at once, and find results in the `rq2` folder as tex files.

#### RQ3

For tables from RQ3, there exists a script to automatically gather and collate all input data from the relevant files, `gather_inputs_rq3.py`. Find it and set the relevant parameters to the desired outcome (`target_charac` and `target_mode`) and run the script. It will automatically save the result of your run in the `oldinputs` folder. Then, run the `to_latex.py` script.

Alternatively, use the `full_rq3.py` file, and find results for all tables in the `rq3` folder as tex files.

### Oldinputs

The oldinputs folder is there because many tables require manual editing. They serve as examples and may not contain currently-valid data.

## `full_rq3.py`, `gather_inputs_rq3`, folder `rq3`, `rq2.py`, folder `rq2`

These scripts are automated repetitions for their respective research question's data, using the `to_latex.py` script. The `rq2` and `rq3` folders are generated by their respective scripts. The `gather_inputs_rq3.py` is an intermediate script and does not need to be used if `full_rq3.py` is already used.

## `sting.py`, `sting_cache.json`

This script serves to manually double check database validity: namely, does it list all the comments and votes available for an issue?

## `projects_to_latex.py`, `projects.tex`

This script generates the domain-projects table list as seen in the relevant thesis appendix.

## `high_conf_graphics.py` and the folder `highconf_tex`

This script and the resulting folder of result folders gather up all of the high-confidence versions of the results, all the same graphics that are also in the thesis (main body + appendix), and deposit them into the `highconf_tex` folder so that one can generate a report to view the results more easily. The folder also has the required `main.tex` and a rendered `.pdf`.