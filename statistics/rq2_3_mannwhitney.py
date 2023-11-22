import os
import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import json

import config as c


def perform_tests(rawdata, charac, xticks, folder, filename_extra="", labels=[], outliers=False, method="auto", width=8, show_legend=True):
    os.makedirs(os.path.dirname(f'results/mannwhitney/{folder}/'), exist_ok=True)
    greater_than = {}
    less_than = {}

    domains = list(rawdata.keys())
    dtypes = list(rawdata[domains[0]].keys())

    # the csv
    csv = ","
    # column headers
    for dtype in dtypes:
        for dom in domains:
            csv += f"{dtype}-{dom},"
    csv += '\n'

    # each row
    for xi in range(len(dtypes)):
        x_dtype = dtypes[xi]
        for xj in range(len(domains)):
            x_dom = domains[xj]
            rowheader = f"{x_dtype}-{x_dom}"
            results = [rowheader]
            for yi in range(len(dtypes)):
                y_dtype = dtypes[yi]
                for yj in range(len(domains)):
                    y_dom = domains[yj]
                    if (xi*len(domains) + xj) >= (yi*len(domains) + yj):
                        results.append('')
                        continue
                    if 0 in [len(rawdata[x_dom][x_dtype]), len(rawdata[y_dom][y_dtype])]:
                        results.append('')
                        continue

                    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
                    res = mannwhitneyu(rawdata[x_dom][x_dtype], rawdata[y_dom][y_dtype], alternative="two-sided", method=method)
                    value = f"Equal ({res.pvalue})"
                    if res.pvalue < 0.05:
                        res = mannwhitneyu(rawdata[x_dom][x_dtype], rawdata[y_dom][y_dtype], alternative="less", method=method)
                        value = "Less" if res.pvalue < 0.05 else "Greater"
                        if value == "Greater":
                            if not x_dom in greater_than:
                                greater_than[x_dom] = {}
                            if not x_dtype in greater_than[x_dom]:
                                greater_than[x_dom][x_dtype] = {}
                            if not y_dom in greater_than[x_dom][x_dtype]:
                                greater_than[x_dom][x_dtype][y_dom] = {}
                            greater_than[x_dom][x_dtype][y_dom][y_dtype] = 1 - res.pvalue
                        else:
                            if not x_dom in less_than:
                                less_than[x_dom] = {}
                            if not x_dtype in less_than[x_dom]:
                                less_than[x_dom][x_dtype] = {}
                            if not y_dom in less_than[x_dom][x_dtype]:
                                less_than[x_dom][x_dtype][y_dom] = {}
                            less_than[x_dom][x_dtype][y_dom][y_dtype] = res.pvalue
                        value += f" ({res.pvalue})"

                    results.append(value)
            csv += ",".join(results) + ",\n"

    # save csv
    with open(f'results/mannwhitney/{folder}/{charac}{filename_extra}.csv', 'w') as f:
        f.write(csv)

    # box plot
    margins = 0.1
    space_per_dom = (1.0 - margins*2.0) / len(domains)
    plt.figure().set_figwidth(width)
    locations = {}
    for i in range(len(domains)):
        dom = domains[i]
        this_dom = []
        for dtype in dtypes:
            this_dom.append(rawdata[dom][dtype])
        this_plot = plt.boxplot(this_dom, positions=np.array(np.arange(len(this_dom)))+(i+1)*space_per_dom, widths=space_per_dom*0.90, showfliers=outliers)
        
        for k, v in this_plot.items():
            plt.setp(this_plot.get(k), color=c.colors[i])

        locations[dom] = {}
        for j in range(len(dtypes)):
            x = this_plot['caps'][j*2]._x
            x = (x[0] + x[1])* 0.5
            y = this_plot['caps'][j*2+1]._y[0]
            locations[dom][dtypes[j]] = [(x, y), this_plot['caps'][j*2]._color]

        label = dom.title() if len(labels) == 0 else labels[i]
        plt.plot([], c=c.colors[i], label=label)
        if show_legend:
            plt.legend()
    
    x_offset = 0

    for dom in domains:
        x_offset += locations[dom][dtypes[0]][0][0]
    x_offset = x_offset / len(domains)

    plt.xticks(np.arange(len(dtypes))+x_offset, xticks)
    plt.title(charac.title()) # todo correct? from "ch.title()"
    plt.savefig(f'results/mannwhitney/{folder}/{charac}{filename_extra}_plot.png', bbox_inches="tight")

    # with arrows
    radsize = ".8" if width > 8 else ".4"
    arrow_cutoff = 0.001
    for x_dom in greater_than:
        for x_dtype in greater_than[x_dom]:
            for y_dom in greater_than[x_dom][x_dtype]:
                if x_dtype in greater_than[x_dom][x_dtype][y_dom] and greater_than[x_dom][x_dtype][y_dom][x_dtype] < arrow_cutoff:
                    start = locations[x_dom][x_dtype][0]
                    end = locations[y_dom][x_dtype][0]
                    kw = dict(arrowstyle=c.style, color=locations[x_dom][x_dtype][1])
                    plt.gca().add_patch(patches.FancyArrowPatch(start, end, connectionstyle=f"arc3, rad=-{radsize}", **kw))
    for x_dom in less_than:
        for x_dtype in less_than[x_dom]:
            for y_dom in less_than[x_dom][x_dtype]:
                if x_dtype in less_than[x_dom][x_dtype][y_dom] and less_than[x_dom][x_dtype][y_dom][x_dtype] < arrow_cutoff:
                    end = locations[x_dom][x_dtype][0]
                    start = locations[y_dom][x_dtype][0]
                    kw = dict(arrowstyle=c.style, color=locations[y_dom][x_dtype][1])
                    plt.gca().add_patch(patches.FancyArrowPatch(start, end, connectionstyle=f"arc3, rad={radsize}", **kw))
    ylims = plt.ylim()
    plt.ylim(ylims[0], ylims[1] * 1.2)
    plt.savefig(f'results/mannwhitney/{folder}/{charac}{filename_extra}_plot_arrows.png', bbox_inches="tight")

    # done :)
    plt.close('all')

# legend
os.makedirs(os.path.dirname('results/mannwhitney/'), exist_ok=True)
for i in range(len(c.domains)):
    dom = c.domains[i]
    label = dom.title()
    plt.plot([], c=c.colors[i], label=label)
    plt.legend()
plt.savefig(f'results/mannwhitney/domlegend.png', bbox_inches='tight')

def mannwhitney_rq2(name = ""):
    rawdata = c.get_data_rq2(name)

    for ch in c.charac_cont:
        mwdata = {'': rawdata[ch]}
        mwdata = {}
        for dom in rawdata[ch]:
            mwdata[dom] = {'': rawdata[ch][dom]}
        perform_tests(mwdata, ch, [''], f'rq2_{ch}', filename_extra=name, show_legend = False)
        perform_tests(mwdata, ch, [''], f'rq2_{ch}', outliers=True, filename_extra=f"_fliers{name}", show_legend = False)

def mannwhitney_rq3(name = ""):
    for ch in c.charac_cont:
        # intersected dtypes
        rawdata = {"full": {}}
        for dom in c.domains:
            with open(f"data/domain_{dom}{name}.json") as f:
                rawdata[dom] = {}
                this_dom = json.load(f)
                for dtype in c.dtypes:
                    if not dtype in rawdata['full']:
                        rawdata['full'][dtype] = []
                    
                    if dtype not in this_dom:
                        rawdata[dom][dtype] = []
                        continue
                    if ch not in this_dom[dtype]:
                        rawdata[dom][dtype] = []
                        continue
                    rawdata[dom][dtype] = this_dom[dtype][ch]

                    rawdata['full'][dtype].extend(this_dom[dtype][ch])
        
        perform_tests(rawdata, ch, c.dtypes_short, f'rq3_{ch}', filename_extra=name, width = 18)
        perform_tests({'full': rawdata['full']}, ch, c.dtypes_short, f'rq3_{ch}', filename_extra=f'_full_only{name}', width = 8)

        # inverted
        rawdata_inverted = {}
        for dom in rawdata:
            for dtype in rawdata[dom]:
                if not dtype in rawdata_inverted:
                    rawdata_inverted[dtype] = {}
                rawdata_inverted[dtype][dom] = rawdata[dom][dtype]

        replacement = {
            "existence": "Exis",
            "executive": "Exec",
            "existence-executive": "Exis-Exec",
            "property": "Prop",
            "existence-property": "Exis-Prop",
            "executive-property": "Exec-Prop",
            "existence-executive-property": "All",
            "nonarch": "Non-Arch",

            "content management": "CM",
            "data storage & processing": "DSP",
            "devops and cloud": "DC",
            "soa and middlewares": "SOAM",
            "software development tools": "SDT",
            "web development": "WD"
        }
        xticks_this = [replacement[x.lower()] if x.lower() in replacement else x.title() for x in list(rawdata.keys())]
        
        perform_tests(rawdata_inverted, ch, xticks_this, f'rq3_{ch}', filename_extra=f"_inverted{name}", labels=c.dtypes_short, width = 18)

        # simplified dtypes
        rawdata_simple = {}
        for dom in rawdata:
            rawdata_simple[dom] = {}
            for dtype_comb in c.dtype_combined:
                rawdata_simple[dom][dtype_comb] = []
                for dtype_orig in c.dtype_combined[dtype_comb]:
                    rawdata_simple[dom][dtype_comb].extend(rawdata[dom][dtype_orig])

        simple_xticks = [x.title() for x in list(c.dtype_combined.keys())]
        perform_tests(rawdata_simple, ch, simple_xticks, f'rq3_{ch}', filename_extra=f"_simple{name}", width = 12)
        perform_tests({'full': rawdata_simple['full']}, ch, simple_xticks, f'rq3_{ch}', filename_extra=f"_simple_full_only{name}", width = 4)
        
        rawdata_simple_inverted = {}
        for dom in rawdata_simple:
            for dtype in rawdata_simple[dom]:
                if not dtype in rawdata_simple_inverted:
                    rawdata_simple_inverted[dtype] = {}
                rawdata_simple_inverted[dtype][dom] = rawdata_simple[dom][dtype]

        labels_this = [replacement[x.lower()] if x.lower() in replacement else x.title() for x in list(rawdata_simple.keys())]
        
        perform_tests(rawdata_simple_inverted, ch, labels_this, f'rq3_{ch}', filename_extra=f"_simple_inverted{name}", labels=simple_xticks, width = 12)

        print(f"RQ3 Mann-Whitney {name}: {ch} done")

mannwhitney_rq3("_high_conf")
mannwhitney_rq3()

mannwhitney_rq2()
mannwhitney_rq2("_high_conf")
