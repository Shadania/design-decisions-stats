from gather_inputs_rq3 import get_result


characs = ["has_pdf", "hierarchy", "issue_type", "resolution", "status"]
modes = [
    # "intersected_high_conf", "simple_high_conf",
    "intersected", "simple"
]

for ch in characs:
    for m in modes:
        get_result(ch, m)