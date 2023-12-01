from to_latex import run

characs = ["has_pdf", "hierarchy", "issue_type", "resolution", "status"]

def toheader(domain):
    if domain == "full":
        return "all domains"
    return domain

# modes can be [''] for regular or ['_high_conf']

def run_rq2(modes = [''], copyto=None):
    for ch in characs:
        for m in modes:
            result = []
            with open(f"../statistics/results/chisq/rq2_{ch}{m}.csv") as f:
                mode = "scan"
                for line in f.readlines():
                    match mode:
                        case 'scan':
                            if line.strip() == "value/expected":
                                mode = "header"
                            continue
                        case 'header':
                            result.append("Domains"+line.strip())
                            mode = "read"
                            continue
                        case 'read':
                            result.append(line.strip())
                            continue
            result = '\n'.join(result)
            with open('input.txt', 'w') as f:
                f.write(result)
            with open(f'oldinputs/rq2_{ch}{m}', 'w') as f:
                f.write(result)
            
            filename = f'rq2/table_{ch}{m}.tex'
            run(f'rq2/table_{ch}{m}')
            if copyto is not None:
                import shutil
                shutil.copy(filename, copyto+f'table_{ch}{m}.tex')

if __name__ == '__main__':
    run_rq2()