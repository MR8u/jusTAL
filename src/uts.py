def parse_tsv(tsv):
    uts = []
    for line in tsv.split('\n')[3:]:
        if line.strip() == '':
            continue
        if line.startswith('#'):
            uts.append([])
            continue
        uts[-1].append(line.strip().split('\t'))
    return uts

def parse_ut(ut):
    tokens = []
    for tid, cid, t, st, rv, rco in ut:
        if st == 'TARGET':
            t = t[:-1] + f' type="{rv}">'
        tokens.append(t)
    return ' '.join(tokens)

def parse_files(paths):
    uts = []
    for path in paths:
        for i, ut in enumerate(parse_tsv(path.read_text(encoding='utf-8'))):
            uts.append((path.stem, i, parse_ut(ut)))
    return uts

def get_president_reporter(ut):
    s = list(ut.children)[0].split()
    return s[0], s[1] if len(s) > 1 else None

def parse_name(x, president, reporter):
    n = x[1:].split('_')[0].capitalize()
    if x == president:
        return f'le président {n}'
    if x == reporter:
        return f'le rapporteur {n}'
    return f'monsieur {n}'