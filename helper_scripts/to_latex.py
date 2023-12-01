red = [0.76, 0.13, 0.28]
yellow = [0.91, 0.84, 0.42]
green = [0.53, 0.66, 0.42]

def rendercol(col):
    return '{'+f"{col[0]},{col[1]},{col[2]}"+'}'

def lerp(a, b, value):
    return a*value + b*(1-value)

def lerpcol(colA, colB, value):
    result = []
    for i in range(len(colA)):
        result.append(lerp(colA[i], colB[i], value))
    return result

def process_value(value, minval, maxval):
    value = value.title()
    replacement = {
        "Existence": "Exis",
        "Executive": "Exec",
        "Existence-Executive": "Exis-Exec",
        "Property": "Prop",
        "Existence-Property": "Exis-Prop",
        "Executive-Property": "Exec-Prop",
        "Existence-Executive-Property": "All",
        "Nonarch": "Non-Arch",

        "Content Management": "CM",
        "Data Storage \\& Processing": "DSP",
        "Devops And Cloud": "DC",
        "Soa And Middlewares": "SOAM",
        "Software Development Tools": "SDT",
        "Web Development": "WD"
    }
    try:
        floatval = float(value)
        result = "{:.2f}".format(floatval)

        if floatval <= 1.0:
            alpha = (floatval - minval) / (1 - minval)
            targetcol = lerpcol(red, yellow, 1-alpha)
        else:
            alpha = (floatval - 1) / (maxval - 1)
            targetcol = lerpcol(yellow, green, 1-alpha)
        result = f"\\cellcolor[rgb]{rendercol(targetcol)} " + result

        return result
    except:
        return replacement[value] if value in replacement else value

def run(output="output", input='input.txt'):
    with open(input) as f:
        values = [line.strip().replace('&', '\\&').split(',') for line in f.readlines()]

    with open(f'{output}.tex', 'w') as f:
        actual_numbers = []
        for arr in values:
            for x in arr:
                try:
                    val = float(x)
                    actual_numbers.append(val)
                except:
                    continue

        minval = min(actual_numbers)
        maxval = max(actual_numbers)
        amtcols = len(values[0])
        f.write(f"\\begin{{tabular}}{{{'|c||'+'c|'*(amtcols - 1)}}}")
        f.write('\n\\hline\n')

        for arr in values:
            if len(arr) == 1:
                f.write('\\hline\n')
                continue
            results = []
            while len(arr) > amtcols:
                arr.pop()
            for x in arr:
                results.append(process_value(x, minval, maxval))
            f.write(' & '.join(results))
            f.write(' \\\\ \n\\hline\n')

        f.write('\\end{tabular}')

if __name__ == '__main__':
    run()