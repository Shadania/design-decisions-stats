from to_latex import run

characs = ["has_pdf", "hierarchy", "issue_type", "resolution", "status"]
modes = [
    ""# , "_high_conf"
]

def toheader(domain):
    if domain == "full":
        return "all domains"
    return domain

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
        
        run(f'rq2/table_{ch}{m}')
