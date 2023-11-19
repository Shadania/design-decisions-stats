from scipy.stats import chi2_contingency
import numpy as np
import json
import pylab as plt
from matplotlib_venn import venn3
import config as c
import os

def run_chi_sq(values, filename, rowheaders, colheaders):
    data = np.array(values)

    # total_sum values change depending on data used
    total_sum = sum([sum(x) for x in values])

    answer = []
    pvals = []
    expected_vals = []
    for row in range(0,len(values)):
        answer.append([])
        pvals.append([])
        expected_vals.append([])
        for col in range(0,len(values[0])):
            # get the 4 values for the contingency table (2x2 matrix):
            # [current, right],
            # [bottom, bottom_right]
            
            current = data[row,col]
            row_sum = sum(data[row])
            col_sum = sum(data[:,col])
            right = row_sum-current
            bottom = col_sum-current
            
            bottom_right = total_sum - row_sum - col_sum + current
            
            # create table for each co-occurence
            contingency_table = np.array(
                [
                    [current, right],
                    [bottom, bottom_right]
                ])
            
            # documentation for function: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
            # the h0 used is independence of variables. so a significant p-value means dependence
            # more explanations: https://www.askpython.com/python/examples/chi-square-test
            if (0 in contingency_table[0]) or (0 in contingency_table[1]):
                answer[-1].append('null')
                pvals[-1].append(2)
                expected_vals[-1].append('null')
            else:
                stat, p, dof, expected  = chi2_contingency(contingency_table)
            
                # create table of all co-occurences
                answer[-1].append(stat)
                pvals[-1].append(p)
                expected_vals[-1].append(expected[0][0])


    os.makedirs(os.path.dirname('results/rq1/'), exist_ok=True)

    with open(f"results/rq1/{filename}.json", 'w') as f:
        json.dump({"stats": answer, "pvals": pvals, "expected": expected_vals}, f)
    with open(f"results/rq1/{filename}.csv", 'w') as f:
        f.write('values\n')
        f.write(','.join(['']+colheaders)+'\n')
        idx = 0
        for row in values:
            f.write(','.join([rowheaders[idx]] + [str(x) for x in row])+"\n")
            idx += 1

        f.write('\nstats\n')
        f.write(','.join(['']+colheaders)+'\n')
        idx = 0
        for row in answer:
            f.write(','.join([rowheaders[idx]] + [str(x) for x in row])+"\n")
            idx += 1

        f.write('\npvals\n')
        f.write(','.join(['']+colheaders)+'\n')
        idx = 0
        for row in pvals:
            f.write(','.join([rowheaders[idx]] + [str(x) if x>0.001 else '0' for x in row])+'\n')
            idx += 1

        f.write('\nexpected\n')
        f.write(','.join(['']+colheaders)+'\n')
        idx = 0
        for row in expected_vals:
            f.write(','.join([rowheaders[idx]] + [str(x) for x in row])+'\n')
            idx += 1

        f.write('\nvalue/expected\n')
        f.write(','.join(['']+colheaders)+'\n')
        for row in range(0, len(rowheaders)):
            f.write(rowheaders[row]+',')
            for col in range(0, len(colheaders)):
                f.write(f"{values[row][col]/expected_vals[row][col] if pvals[row][col] < 0.05 else ''},")
            f.write('\n')

labelformatstr = "\n{:.1f}%"
subsetlabelsize = 11

def run_rq1(name = ""):
    with open(f'data/counts{name}.json') as f:
        count_data = json.load(f)

    single_label_counts = []
    multi_label_counts = []

    for dom in c.domains:
        single_label_counts.append([])
        for dtype_comb in c.dtype_combined:
            count = 0
            for dtype_orig in c.dtype_combined[dtype_comb]:
                count += count_data[dom][dtype_orig]
            single_label_counts[-1].append(count)

        multi_label_counts.append([])
        for dtype in c.dtypes:
            multi_label_counts[-1].append(count_data[dom][dtype])

    run_chi_sq(single_label_counts, f'chi2_single{name}', c.domains, list(c.dtype_combined.keys()))
    run_chi_sq(multi_label_counts, f'chi2_multi{name}', c.domains, c.dtypes)

    # plotting
    total = {}
    full_total = 0

    for dom in count_data:
        dom_total = 0
        for label in count_data[dom]:
            if not label in total:
                total[label] = 0
            total[label] += count_data[dom][label]
            dom_total += count_data[dom][label]
            full_total += count_data[dom][label]

        v = venn3(subsets=(
            count_data[dom]['existence'],
            count_data[dom]['executive'],
            count_data[dom]['existence-executive'],
            count_data[dom]['property'],
            count_data[dom]['existence-property'],
            count_data[dom]['executive-property'],
            count_data[dom]['existence-executive-property']
        ), 
        set_labels=('Existence', 'Executive', 'Property'),
        subset_label_formatter=lambda x: str(x) + labelformatstr.format((float(x)/dom_total)*100))
        plt.suptitle(dom.title() + f" - Total Issues: {dom_total}")
        plt.title(f"Non-architectural issues: {count_data[dom]['']} ({'{:.02f}'.format(count_data[dom]['']/float(dom_total) * 100)}%)")
        for text in v.subset_labels:
            if text:
                text.set_fontsize(subsetlabelsize)
        plt.tight_layout()
        plt.savefig(f"results/rq1/{dom}_counts{name}.png", bbox_inches="tight", pad_inches=0)
        plt.clf()



    v = venn3(subsets=(
        total['existence'],
        total['executive'],
        total['existence-executive'],
        total['property'],
        total['existence-property'],
        total['executive-property'],
        total['existence-executive-property']
    ), 
    set_labels=('Existence', 'Executive', 'Property'),
    subset_label_formatter=lambda x: str(x) + labelformatstr.format((float(x)/full_total)*100))
    plt.suptitle(f"Across All Domains - Total Issues: {full_total}")
    plt.title(f"Non-architectural issues: {total['']} ({'{:.02f}'.format(total['']/float(full_total) * 100)}%)")
    for text in v.subset_labels:
        if text:
            text.set_fontsize(subsetlabelsize)
    plt.tight_layout()
    plt.savefig(f"results/rq1/total_counts{name}.png", bbox_inches="tight", pad_inches=0)
    plt.clf()

run_rq1()
run_rq1("_high_conf")