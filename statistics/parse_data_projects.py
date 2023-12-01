import json
import config as c


def run(name=''):
    # project - labels (RQ1)
    with open(f'data/projects/all.json') as f:
        projects = json.load(f)

    proj_counts = {}
    for proj in projects:
        with open(f'data/projects/{proj}_counts{name}.json') as f:
            proj_counts[proj] = json.load(f)
    with open(f"results/projects/{proj}_counts{name}.csv", 'w') as f:
        with open(f"results/projects/{proj}_counts{name}_percents.csv", 'w') as w:
            # header
            header = 'Project' + ',' + ','.join(c.dtypes_short)
            f.write(header+',Total\n')
            w.write(header+'\n')
            # all projects
            for proj in projects:
                f.write(proj + ',')
                w.write(proj + ',')
                this_line = []
                this_total = 0
                for dt in c.dtypes:
                    this_total += proj_counts[proj][dt]
                    this_line.append(proj_counts[proj][dt])
                f.write(','.join(this_line) + f",{this_total}\n")
                w.write(','.join(["{.2f}%".format(float(x) / this_total * 100.0) for x in this_line]) + '\n')

    # project - characteristics (RQ2)
    # chi-squared chars first
    for char in c.charac_categ:
        proj_chars = {}
        all_values = []
        for proj in projects:
            with open(f"data/projects/{proj}_chars{name}.json") as f:
                proj_chars[proj] = json.load(f)[char]
                for value in proj_chars[proj]:
                    if not value in all_values:
                        all_values.append(value)
        with open(f"results/projects/{proj}_{char}{name}.csv", 'w') as f:
            with open(f"results/projects/{proj}_{char}{name}_percents.csv", 'w') as w:
                header = char + ',' + ','.join(all_values)
                f.write(header + ',Total\n')
                w.write(header + '\n')

                for proj in proj_chars:
                    f.write(proj+',')
                    w.write(proj+',')
                    this_line = []
                    this_total = 0
                    for val in all_values:
                        if not val in proj_chars[proj]:
                            this_line.append(0)
                        else:
                            this_line.append(proj_chars[proj][val])
                        this_total += this_line[-1]
                    f.write(','.join(this_line) + f',{this_total}\n')
                    w.write(','.join(["{.2f}%".format(float(x) / this_total * 100.0) for x in this_line]) + '\n')

    # now the mann-whitney
    for char in c.charac_cont:
        proj_chars = {}
        for proj in projects:
            with open(f"data/projects/{proj}_chars{name}.json") as f:
                proj_chars[proj] = json.load(f)[char]
        


import os
os.makedirs("results/projects/", exist_ok=True)

run()
run('_high_conf')