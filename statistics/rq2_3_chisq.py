import json
import os
from scipy.stats import chi2_contingency
import numpy as np

import config as c

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
    
    os.makedirs(os.path.dirname(filename+'.json'), exist_ok=True)

    with open(filename+".json", 'w') as f:
        json.dump({"values": values, "stats": answer, "pvals": pvals, "expected": expected_vals}, f)
    with open(filename+".csv", 'w') as f:
        f.write('values\n')
        idx = 0
        f.write(','.join([''] + colheaders)+'\n')
        for row in values:
            f.write(','.join([rowheaders[idx]] + [str(x) for x in row])+'\n')
            idx += 1

        f.write('\nstats\n')
        idx = 0
        f.write(','.join([''] + colheaders)+'\n')
        for row in answer:
            f.write(','.join([rowheaders[idx]] + [str(x) for x in row])+"\n")
            idx += 1
        
        f.write('\npvals\n')
        idx = 0
        f.write(','.join([''] + colheaders)+'\n')
        for row in pvals:
            f.write(','.join([rowheaders[idx]] + [str(x) if x>0.001 else '0' for x in row])+'\n')
            idx += 1

        f.write('\nexpected\n')
        idx = 0
        f.write(','.join([''] + colheaders)+'\n')
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

# categorical characteristics: this will look like a table that i can just chisq.
# rows are domains. columns are values. per characteristic. graph it with bars?
def run_tests_rq2(name = ""):
    rawdata = c.get_data_rq2(name)
    for ch in c.charac_categ:
        # compile csv
        values = []
        for dom in rawdata[ch]:
            for val in rawdata[ch][dom]:
                if not val in values:
                    if ch in c.values_to_count and val not in c.values_to_count[ch]:
                        continue
                    values.append(val)

        data = []
        for dom in c.domains:
            data.append([])
            for val in values:
                data[-1].append(rawdata[ch][dom][val] if val in rawdata[ch][dom] else 0)

        run_chi_sq(data, f'results/chisq/rq2_{ch}{name}', c.domains, values)

def run_tests_rq3(dtypemode = "intersected", name = ""):
    dtypes_to_check = c.dtypes if dtypemode == "intersected" else list(c.dtype_combined.keys())

    # per domain, per characteristic
    for dom in c.domains:
        with open(f'data/domain_{dom}{name}.json') as f:
            domdata = json.load(f)
        # columns are decision types
        # rows are values for the characteristic
        for ch in c.charac_categ:
            chardata = {} # option -> dtype -> numbers
            if (dtypemode == "intersected"):
                for dtype in c.dtypes:
                    if dtype not in domdata:
                        continue
                    if ch not in domdata[dtype]:
                        continue
                    for option in domdata[dtype][ch]:
                        if ch in c.option_limiting:
                            if option not in c.option_limiting[ch]:
                                continue
                        if not option in chardata:
                            chardata[option] = {}
                        chardata[option][dtype] = domdata[dtype][ch][option]
            else:
                for dtype_comb in c.dtype_combined:
                    for dtype_orig in c.dtype_combined[dtype_comb]:
                        if dtype_orig not in domdata:
                            continue
                        if ch not in domdata[dtype_orig]:
                            continue
                        for option in domdata[dtype_orig][ch]:
                            if ch in c.option_limiting:
                                if option not in c.option_limiting[ch]:
                                    continue
                            if not option in chardata:
                                chardata[option] = {}
                            if not dtype_comb in chardata[option]:
                                chardata[option][dtype_comb] = 0
                            chardata[option][dtype_comb] += domdata[dtype_orig][ch][option]

            chardata_arr = []
            option_list = []

            for option in chardata:
                option_list.append(option)
                chardata_arr.append([])
                
                for dtype in dtypes_to_check:
                    chardata_arr[-1].append(chardata[option][dtype] if dtype in chardata[option] else 0)
            run_chi_sq(chardata_arr, f"results/chisq/rq3_{ch}/{dom}_{dtypemode}{name}", option_list, dtypes_to_check)

    # per characteristic, cross-domain
    for ch in c.charac_categ:
        chardata = {}
        for dom in c.domains:
            with open(f"data/domain_{dom}{name}.json") as f:
                domdata = json.load(f)
            if dtypemode == "intersected":
                for dtype in c.dtypes:
                    if dtype not in domdata:
                        continue
                    if ch not in domdata[dtype]:
                        continue
                    for option in domdata[dtype][ch]:
                        if ch in c.option_limiting:
                            if option not in c.option_limiting[ch]:
                                continue
                        if not option in chardata:
                            chardata[option] = {}
                        if not dtype in chardata[option]:
                            chardata[option][dtype] = 0
                        chardata[option][dtype] += domdata[dtype][ch][option]
            else:
                for dtype_comb in c.dtype_combined:
                    for dtype_orig in c.dtype_combined[dtype_comb]:
                        if dtype_orig not in domdata:
                            continue
                        if ch not in domdata[dtype_orig]:
                            continue
                        for option in domdata[dtype_orig][ch]:
                            if ch in c.option_limiting and option not in c.option_limiting[ch]:
                                continue

                            if not option in chardata:
                                chardata[option] = {}
                            if not dtype_comb in chardata[option]:
                                chardata[option][dtype_comb] = 0
                            chardata[option][dtype_comb] += domdata[dtype_orig][ch][option]
        
        chardata_arr = []
        option_list = []

        for option in chardata:
            option_list.append(option)
            chardata_arr.append([])

            for dtype in dtypes_to_check:
                chardata_arr[-1].append(chardata[option][dtype] if dtype in chardata[option] else 0)
        run_chi_sq(chardata_arr, f"results/chisq/rq3_{ch}/full_{dtypemode}{name}", option_list, dtypes_to_check)

run_tests_rq2()
run_tests_rq2("_high_conf")

run_tests_rq3()
run_tests_rq3("simple")
run_tests_rq3(name="_high_conf")
run_tests_rq3("simple", "_high_conf")