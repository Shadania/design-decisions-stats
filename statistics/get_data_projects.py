from nltk.corpus import stopwords
import requests
requests.packages.urllib3.disable_warnings() 
import json
from datetime import datetime
import config as c

stop = set(stopwords.words('english'))

# helper functions

def count_words(str):
    if str is None:
        return 0
    if c.keep_format:
        return len(str.split())
    else:
        stop = set(stopwords.words('english'))
        return len([x for x in str.lower().split() if x not in stop])

def avg_len(list_of_str):
    sum = 0
    for str in list_of_str:
        sum += count_words(str)
    return float(sum) / len(list_of_str)

def get_duration(issue_dic):
    datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z" # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    if not 'created' in issue_dic:
        return None
    created_dt = datetime.strptime(issue_dic['created'], datetime_format)
    del issue_dic['created']
    if 'resolutiondate' in issue_dic and issue_dic['resolutiondate'] is not None:
        resolved_dt = datetime.strptime(issue_dic['resolutiondate'], datetime_format)
        del issue_dic['resolutiondate']
    else:
        return None
    return (resolved_dt - created_dt).days


def count(conf_req = {"existence": 0, "executive": 0, "property": 0}, name = ""):
    ecosys = requests.get(f"{c.db_url}/projects", verify=False).json()
    projects = []
    for e in ecosys:
        # let's still keep to the "only significant projects" rule
        if 'merged_domain' in e['additional_properties']:
            projects.append(f"{e['ecosystem']}-{e['key']}")

    with open('data/projects/all.json', 'w') as f:
        json.dump(projects, f)
    
    # per project, grab all issue IDs, and do counts
    proj_counts = {}
    for proj in projects:
        proj_counts = {
            "existence": 0,
            "executive": 0,
            "property": 0,
            "existence-executive": 0,
            "existence-property": 0,
            "executive-property": 0,
            "existence-executive-property": 0,
            '': 0
        }
        
        req_body = {
            "filter": {
                "tags": {
                    "$eq": proj
                }
            }
        }

        proj_issues = requests.get(f"{c.db_url}/issue-ids", json=req_body, verify=False).json()['issue_ids']

        page_size = 3000
        print(f"Getting {len(proj_issues)} issues for project {proj}...")

        next_to_grab = min(page_size, len(proj_issues))
        this_batch = proj_issues[:next_to_grab]
        proj_issues = proj_issues[next_to_grab:]
        
        children = [] # for statistics
        stat_results = {}
        issue_labels = {}

        while (len(proj_issues) + next_to_grab) > 0:
            data = requests.get(f"{c.db_url}/models/{c.model['id']}/versions/{c.model['version']}/predictions", json={'issue_ids': this_batch}, verify=False).json()['predictions']

            # issue decision type counts: RQ1
            labels = ['existence','executive','property']
            for issue in data:
                this_label = []
                for label in labels:
                    if data[issue][label]['prediction'] and data[issue][label]['confidence'] > conf_req[label]:
                        this_label.append(label)
                this_label = '-'.join(this_label)
                proj_counts[this_label] += 1
                issue_labels[issue] = this_label

            # statistics
            statistics = requests.get(f"{c.db_url}/statistics", json={'issue_ids': this_batch}, verify=False).json()['data']
            for issue in statistics:
                statistics[issue]['description size'] = count_words(statistics[issue]['description']) if 'description' in statistics[issue] else 0
                if 'description' in statistics[issue]:
                    del statistics[issue]['description']

                # comments
                statistics[issue]['comment count'] = len(statistics[issue]['comments']) if 'comments' in statistics[issue] else 0
                statistics[issue]['comment avg size'] = None if statistics[issue]['comment count'] == 0 else avg_len(statistics[issue]['comments'])
                if 'comments' in statistics[issue]:
                    del statistics[issue]['comments']

                # hierarchy step 1
                if 'hierarchy' in statistics[issue]:
                    children.extend(statistics[issue]['hierarchy'])
                statistics[issue]['hierarchy'] = 'Parent' if 'hierarchy' in statistics[issue] and len(statistics[issue]['hierarchy']) > 0 else 'Independent'

                # duration
                statistics[issue]['duration'] = get_duration(statistics[issue])

                # resolution
                if statistics[issue]['resolution'] is not None:
                    if statistics[issue]['status'] is None:
                        statistics[issue]['resolution'] = None
                    else:
                        if (statistics[issue]['status'].lower() not in ['closed','resolved','done']):
                            statistics[issue]['resolution'] = None
                        else:
                            statistics[issue]['resolution'] = statistics[issue]['resolution'].lower()
                stat_results[issue] = statistics[issue]

            # loop continuation
            next_to_grab = min(page_size, len(proj_issues))
            this_batch = proj_issues[:next_to_grab]
            proj_issues = proj_issues[next_to_grab:]
        
        for child in children:
            if child in stat_results:
                stat_results[child]['hierarchy'] = "Child"

        proj_chars = {
            "description size": [],
            "comment count": [],
            "comment avg size": [],
            "hierarchy": {},
            "duration": [],
            "issue_type": {},
            "resolution": {},
            "status": {},
            "votes": [],
            "watches": []
        }
        for issue in stat_results:
            """
            this_label = issue_labels[issue]
            if not this_label in proj_chars:
                proj_chars[this_label] = {
                    "description size": [],
                    "comment count": [],
                    "comment avg size": [],
                    "hierarchy": {},
                    "duration": [],
                    "issue_type": {},
                    "resolution": {},
                    "status": {},
                    "votes": [],
                    "watches": []
                }
            """
            # per characteristic saving
            proj_chars['description size'].append(stat_results[issue]['description size'])

            proj_chars['comment count'].append(stat_results[issue]['comment count'])

            if stat_results[issue]['comment avg size'] is not None:
                proj_chars['comment avg size'].append(stat_results[issue]['comment avg size'])

            hier_val = stat_results[issue]['hierarchy']
            if not hier_val in proj_chars['hierarchy']:
                proj_chars['hierarchy'][hier_val] = 0
            proj_chars['hierarchy'][hier_val] += 1

            if stat_results[issue]['duration'] is not None:
                proj_chars['duration'].append(stat_results[issue]['duration'])

            type_val = stat_results[issue]['issue_type'].lower()
            if not type_val in proj_chars['issue_type']:
                proj_chars['issue_type'][type_val] = 0
            proj_chars['issue_type'][type_val] += 1

            res_val = stat_results[issue]['resolution']
            if res_val is not None:
                if not res_val in proj_chars['resolution']:
                    proj_chars['resolution'][res_val] = 0
                proj_chars['resolution'][res_val] += 1

            status_val = stat_results[issue]['status'].lower()
            if not status_val in proj_chars['status']:
                proj_chars['status'][status_val] = 0
            proj_chars['status'][status_val] += 1

            proj_chars['votes'].append(stat_results[issue]['votes'])
            
            proj_chars['watches'].append(stat_results[issue]['watches'])
        
        with open(f'data/projects/{proj}_chars{name}.json', 'w') as f:
            json.dump(proj_chars, f)
        with open(f'data/projects/{proj}_counts{name}.json', 'w') as f:
            json.dump(proj_counts, f)
        

import os
os.makedirs(os.path.dirname('data/projects/'), exist_ok=True)

count()
count({"existence": 0.95, "executive": 0.9, "property": 0.9}, "_high_conf")