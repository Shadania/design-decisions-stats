from gather_inputs_rq3 import get_result

domains = [
    "content management",
    "data storage & processing",
    "devops and cloud",
    "soa and middlewares",
    "software development tools",
    "web development"
]


characs = ["has_pdf", "hierarchy", "issue_type", "resolution", "status"]
modes = [
    # "intersected_high_conf", "simple_high_conf",
    "intersected", "simple"
]

for ch in characs:
    for m in modes:
        get_result(ch, m)
    get_result(ch, 'simple', ['full'], '_full')
    get_result(ch, 'simple', domains, '_not_full')