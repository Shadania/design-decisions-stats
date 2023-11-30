import json
import config as c

characs = [
    "status",
    "issue_type",
    "resolution"
]

default_jira_options = {
    "issue_type": [ # https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/
        "task", "subtask", # "Business" project types
        "epic", "bug", "story", "task", "subtask", # "Software" project types
        "change", "it help", "incident", "new feature", "problem", "service request", "service request with approval", "support" # service
    ],
    "resolution": [ # https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/
        "done", "won't do", "duplicate", # default
        "cannot reproduce", # with software projects
        "known error", "hardware failure", "software failure" # service management
    ],
    "status": [ # https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/ (not using all, e.g. skipping the recruitment and lead tracking project types)
        "open", "in progress", "done", "to do", "in review", "under review", "approved", "cancelled", "rejected", # default
        "reopened", "resolved", "closed", "building", "build broken", "backlog", "selected for development", # software
        "declined", "waiting for support", "waiting for customer", "pending", "canceled", # halfway through service management - yes this one with one l and the default one with two l's.
        "escalated", "waiting for approval", "awaiting cab approval", "planning", "awaiting implementation", "implementing", "peer review/change manager approval", "work in progress", "completed", "under investigation" # done with service management. whoa
    ]
}

archonly = True

def count(types = None, name = ''):
    results = {}
    for ch in characs:
        this_charac_value_counts = {}
        for dom in c.domains:
            with open(f'data/domain_{dom}.json') as f:
                domdata = json.load(f)
            for dtype in domdata:
                if archonly and dtype == '':
                    continue
                if ch in domdata[dtype]:
                    for option in domdata[dtype][ch]:
                        if types is not None and ch in types and option.lower() not in types[ch]:
                            continue
                        if option not in this_charac_value_counts:
                            this_charac_value_counts[option] = [0, {}]
                        this_charac_value_counts[option][0] += domdata[dtype][ch][option]
                        if dom not in this_charac_value_counts[option][1]:
                            this_charac_value_counts[option][1][dom] = 0
                        this_charac_value_counts[option][1][dom] += domdata[dtype][ch][option]
        results[ch] = sorted(this_charac_value_counts.items(), key=lambda x: x[1][0], reverse=True)

    with open(f"data/values_counted{name}{'_archonly' if archonly else ''}.json", 'w') as f:
        json.dump(results, f)

count()
count(default_jira_options, '_jira_defaults')

def count_inverse():
    results = {}
    for dom in c.domains:
        results[dom] = {}
        with open(f"data/domain_{dom}.json") as f:
            domdata = json.load(f)
        for ch in characs:
            results[dom][ch] = {}
            for dtype in domdata:
                if archonly and dtype == '':
                    continue
                if ch in domdata[dtype]:
                    for option in domdata[dtype][ch]:
                        if option not in results[dom][ch]:
                            results[dom][ch][option] = 0
                        results[dom][ch][option] += domdata[dtype][ch][option]
    with open(f"data/values_counted_inverse{'_archonly' if archonly else ''}.json", 'w') as f:
        json.dump(results, f)

count_inverse()