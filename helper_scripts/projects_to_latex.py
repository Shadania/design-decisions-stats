import json

with open('../statistics/data/projects/domain_projects.json') as f:
    data = json.load(f)


def maxint(arr):
    result = arr[0]
    for num in arr[1:]:
        result = num if num > result else result
    return result

with open('projects.tex', 'w') as f:
    doms = [x.title().replace('&', '\&') for x in list(data.keys())]
    
    f.write(f"\\begin{{tabular}}{{{'|'+'c|'*len(doms)}}}")
    f.write('\n\\hline\n')
    f.write(' & '.join(doms) + '\\\\\n\\hline\hline\n')

    print([len(data[x]) for x in data])
    
    maxidx = maxint([len(data[x]) for x in data])
    for i in range(0, maxidx):
        projects = [data[dom][i] if len(data[dom]) > i else '' for dom in data]
        f.write(' & '.join(projects) + '\\\\\n\\hline\n')
    f.write('\\end{tabular}')