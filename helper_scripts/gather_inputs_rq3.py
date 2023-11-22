from to_latex import run

domains = [
    'full',
    "content management",
    "data storage & processing",
    "devops and cloud",
    "soa and middlewares",
    "software development tools",
    "web development"
]

# pick from: "has_pdf", "hierarchy", "issue_type", "resolution", "status"
target_charac = "has_pdf"

# pick from: "simple", "intersected" (or add "_high_conf" to either for that mode)
target_mode = "intersected"


def toheader(domain):
    if domain == "full":
        return "all domains"
    return domain

def get_result(target_charac, target_mode):
    result = []
    for dom in domains:
        with open(f'../statistics/results/chisq/rq3_{target_charac}/{dom}_{target_mode}.csv') as f:
            mode = "scan"
            for line in f.readlines():
                match mode:
                    case 'scan':
                        if line.strip() == "value/expected":
                            mode = "header"
                        continue
                    case 'header':
                        if "simple" in target_mode:
                            # these already have "nonarch" at the end
                            result.append(toheader(dom) + line.strip())
                        else:
                            result.append(toheader(dom) + line.strip() + "non-arch")
                        mode = "read"
                    case "read":
                        result.append(line.strip())
                        continue
        result.append('')

    with open('input.txt', 'w') as f:
        f.write('\n'.join(result))
    with open(f'oldinputs/rq3_{target_charac}_{target_mode}.txt', 'w') as f:
        f.write('\n'.join(result))

    run(f'rq3/{target_charac}_{target_mode}')

if __name__ == '__main__':
    get_result(target_charac, target_mode)