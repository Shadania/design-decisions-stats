# getting data
model = {
    "id": "648ee4526b3fde4b1b33e099",
    "version": "648f1f6f6b3fde4b1b3429cf"
}

db_url = "https://172.22.144.1:8000"

keep_format = False

# filepaths?

# statistics constants
domains = [
    "content management",
    "data storage & processing",
    "devops and cloud",
    "soa and middlewares",
    "software development tools",
    "web development"
]
charac_categ = [
    "hierarchy",
    "issue_type",
    "resolution",
    "status",
    "has_pdf"
]
charac_cont = [
    "description size",
    "comment count",
    "comment avg size",
    "duration",
    "num_attachments",
    "votes",
    "watches",
]
dtypes = [
    "existence",
    "executive",
    "existence-executive",
    "property",
    "existence-property",
    "executive-property",
    "existence-executive-property",
    ""
]
dtypes_arch = [
    "existence",
    "executive",
    "existence-executive",
    "property",
    "existence-property",
    "executive-property",
    "existence-executive-property"
]
dtypes_short = [
    "Exis.",
    "Exec.",
    "Exis-Exec.",
    "Prop.",
    "Exis-Prop.",
    "Exec-Prop.",
    "All",
    "Non-Arch."
]
dtype_combined = {
    "existence": ["existence", "existence-executive", "existence-property", "existence-executive-property"],
    "executive": ["executive", "existence-executive", "executive-property", "existence-executive-property"],
    "property": ["property", "existence-property", "executive-property", "existence-executive-property"],
    "nonarch": [""]
}
values_to_count = {
    "status": ["closed","resolved","open","gathering interest","done","gathering impact"],
    "issue_type": ["bug","improvement","suggestion","task","sub-task","new project"],
    "resolution": ["fixed","done","won't fix","duplicate","invalid","won't do","complete"]
}

# chisq additional settings
# based on top counts (see isolate_big_values.py)
option_limiting = {
    "status": ["closed", "resolved", "open", "gathering interest", "done", "gathering impact"],
    "issue_type": ['bug', 'improvement', 'suggestion', 'task', 'sub-task', 'new project'],
    "resolution": ['fixed', 'done', "won't fix", 'duplicate', 'invalid', "won't do", "complete"]
}

# mann-whitney graphics
colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:pink",
    "cyan",
    "tab:gray",
    "tab:brown",
    "tab:olive",
    "tab:purple"
]
style = "Simple, tail_width=0.5, head_width=4, head_length=8"

# helpers
import json
def get_data_rq2(name = ""):
    rawdata = {}
    for dom in domains:
        with open(f"data/domain_{dom}{name}.json") as f:
            domdata = json.load(f)
        for dt in dtypes_arch:
            if dt not in domdata:
                continue
            for ch in domdata[dt]:
                if not ch in rawdata:
                    rawdata[ch] = {}
                if ch in charac_categ:
                    if not dom in rawdata[ch]:
                        rawdata[ch][dom] = {}
                    for value in domdata[dt][ch]:
                        if not value in rawdata[ch][dom]:
                            rawdata[ch][dom][value] = 0
                        rawdata[ch][dom][value] += domdata[dt][ch][value]
                elif ch in charac_cont:
                    if not dom in rawdata[ch]:
                        rawdata[ch][dom] = []
                    rawdata[ch][dom].extend(domdata[dt][ch])
    return rawdata