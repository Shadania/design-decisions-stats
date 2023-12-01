from gather_inputs_rq3 import get_result
import shutil
import os
from to_latex import run

# chisq variables

# rq3
domains = [
    "content management",
    "data storage & processing",
    "devops and cloud",
    "soa and middlewares",
    "software development tools",
    "web development"
]
characs = [
    # "has_pdf", 
    "hierarchy", 
    "issue_type", 
    "resolution", 
    "status"
    ]

modes = [
    "intersected_high_conf", "simple_high_conf"
]

def fixdirs(destfile):
    os.makedirs('/'.join(destfile.split('/')[:-1]), exist_ok=True)


def copyfile_rq3_chi(ch, m, extra=''):
    src = f"rq3/{ch}_{m}{extra}.tex"
    dest = f'highconf_tex/rq3_chisq/{ch}_{m}{extra}.tex'
    fixdirs(dest)
    shutil.copyfile(src, dest)

for ch in characs:
    for m in modes:
        get_result(ch, m)
        copyfile_rq3_chi(ch, m)
        
    get_result(ch, 'simple_high_conf', ['full'], '_full')
    copyfile_rq3_chi(ch, 'simple_high_conf', '_full')
    get_result(ch, 'simple_high_conf', domains, '_not_full')
    copyfile_rq3_chi(ch, 'simple_high_conf', '_not_full')

# rq2
from rq2 import run_rq2
os.makedirs('highconf_tex/rq2_chisq/', exist_ok=True)
run_rq2(['_high_conf'], copyto='highconf_tex/rq2_chisq/')


# mannwhitney

charac_mw = [
    "description size",
    "comment count",
    "comment avg size",
    "duration",
    # "num_attachments",
    "votes",
    "watches"
]

for ch in charac_mw:
    folder_rq2 = f"../statistics/results/mannwhitney/rq2_{ch}"
    folder_rq3 = f"../statistics/results/mannwhitney/rq3_{ch}"
    suffix_rq3 = [
        '_inverted_high_conf_plot_arrows',
        '_high_conf_plot_arrows',
        '_simple_inverted_high_conf_plot_arrows',
        '_simple_high_conf_plot_arrows'
    ]
    suffix_rq2 = [
        '_high_conf_plot_arrows'
    ]
    for s in suffix_rq3:
        src = f"{folder_rq3}/{ch}{s}.png"
        dest = f"highconf_tex/rq3_mw/{ch}{s}.png"
        fixdirs(dest)
        shutil.copyfile(src, dest)
    for s in suffix_rq2:
        src = f"{folder_rq2}/{ch}{s}.png"
        dest = f"highconf_tex/rq2_mw/{ch}{s}.png"
        fixdirs(dest)
        shutil.copyfile(src, dest)

# rq1

for dom in domains+['total']:
    src = f'../statistics/results/rq1/{dom}_counts_high_conf.png'
    dest = f'highconf_tex/rq1/{dom}_counts_high_conf.png'
    fixdirs(dest)
    shutil.copyfile(src, dest)

modes = ['single', 'multi']
for m in modes:
    src = f"../statistics/results/rq1/chi2_{m}_high_conf.csv"
    txt = f"oldinputs/rq1_{m}_high_conf.txt"
    # to .txt
    with open(src) as f:
        state = 'scan'
        with open(txt, 'w') as w:
            for line in f.readlines():
                match state:
                    case 'scan':
                        if line.strip() == 'value/expected':
                            mode = 'header'
                        continue
                    case 'header':
                        w.write(','.join(['Domain']+line.strip().split()[1:] + ['Non-arch']) + '\n')
                        mode = 'body'
                        continue
                    case 'body':
                        w.write(line)
                        continue
    
    # to .tex
    run(output=f'highconf_tex/rq1/{m}_high_conf', input=txt)