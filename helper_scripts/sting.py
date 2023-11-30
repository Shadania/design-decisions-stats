import requests
requests.packages.urllib3.disable_warnings() 
import random
import json
import webbrowser

use_cache = True

def run():
    print("Loading issue data...")
    issues = {}

    if use_cache:
        with open(f"sting_cache.json") as f:
            issues = json.load(f)
        pass
    else:
        ecosys = requests.get(f"https://localhost:8000/projects", verify=False).json()
        dom_projects = {}
        for e in ecosys:
            if 'merged_domain' in e['additional_properties']:
                dom = e['additional_properties']['merged_domain'][0]
                if not dom in dom_projects:
                    dom_projects[dom] = []
                dom_projects[dom].append(f"{e['ecosystem']}-{e['key']}")


        # grab all issues
        for dom in dom_projects:
            issues[dom] = []
            for tag in dom_projects[dom]:
                req_body = {
                    "filter": {
                        "tags": {
                            "$eq": tag
                        }
                    }
                }
                issue_ids = requests.get(f"https://localhost:8000/issue-ids", json=req_body, verify=False).json()['issue_ids']
                issues[dom].extend(issue_ids)
            print(f"  -Done with domain {dom} (issue count: {len(issues[dom])})")
        with open(f"sting_cache.json", 'w') as f:
            json.dump(issues, f)

    userinput = input(">")
    while len(userinput) == 0:
        for dom in issues:
            
            next_id = issues[dom][random.randint(0, len(issues[dom])-1)]

            # get self-link
            response = requests.get('https://localhost:8000/issue-data', verify=False, json={
                "issue_ids": [next_id],
                "attributes": ["key", "watches"]
            }).json()['data'][next_id]

            selflink = '/'.join(response['watches']['self'].split('/')[:-1])
            selflink_ui = '/'.join(selflink.split('/')[:-5] + ['browse', response['key']])

            # get amount of votes, attachments
            response = requests.get("https://localhost:8000/statistics", json={"issue_ids": [next_id]}, verify=False).json()['data'][next_id]

            amtvotes = response['votes']
            amtcomments = len(response['comments'])

            print(f'Registered amount of votes for issue {next_id} in domain {dom}: {amtvotes}, amount of comments: {amtcomments}.\n{selflink}\n{selflink_ui}\n-----\n')
            webbrowser.open_new_tab(selflink)
            webbrowser.open_new_tab(selflink_ui)
            input('enter to continue')


        userinput = input('>')

run()