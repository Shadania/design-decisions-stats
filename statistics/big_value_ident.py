import json

archonly = True

characs = ['status', 'resolution', 'issue_type']

def tryFormat(val):
    try:
        return "{:.2f}%".format(val)
    except:
        return val

def run():
    with open(f'data/values_counted_inverse{"_archonly" if archonly else ""}.json') as f:
        rawdata = json.load(f)
    
    # preparatory data gathering
    domtotals = {}
    for dom in rawdata:
        domtotals[dom] = 0
        for value in rawdata[dom]['status']:
            domtotals[dom] += rawdata[dom]['status'][value]

    allvalues = {}
    for charac in characs:
        allvalues[charac] = []
        for dom in rawdata:
            for value in rawdata[dom][charac]:
                if value not in allvalues[charac]:
                    allvalues[charac].append(value)

    valuesToUse = {}
    for charac in characs:
        valuesToUse[charac] = []
        for value in allvalues[charac]:
            domsPresentIn = 0
            for dom in rawdata:
                if value in rawdata[dom][charac]:
                    domsPresentIn += 1
            if domsPresentIn >= 3: # cutoff point
                valuesToUse[charac].append(value)

    # write to csv
    with open(f'data/values_ident{"_archonly" if archonly else ""}.csv', 'w') as f:
        for charac in characs:
            f.write(charac + ',' + ','.join(valuesToUse[charac]) + '\n')
            for dom in rawdata:
                results = [dom]
                for value in valuesToUse[charac]:
                    if value not in rawdata[dom][charac]:
                        results.append('')
                    else:
                        results.append(float(rawdata[dom][charac][value]) / domtotals[dom] * 100.0)
                f.write(','.join([tryFormat(x) for x in results]) + '\n')

            f.write('\n')

run()