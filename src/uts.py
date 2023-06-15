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

def parse_sent(ut):
    sents = []
    target_ids, target_types, sent = [], [], []
    for tid, cid, t, st, rv, rco in ut:
        
        if t.startswith('<!--'):
            s = t.split()
            president = s[1]
            reporter = s[2] if len(s) > 3 else None
        
        elif st == 'SPEAKER':
            speaker = t.split('"')[1]
        
        elif st == 'TARGET':
            _id = t.split('"')[1] 
            if len(list(filter(lambda x: x[0] == _id and x[1] == rv, zip(target_ids, target_types)))) == 0:
                target_ids.append(_id)
                target_types.append(rv)

        elif t.strip() in ['.', ';']:
            if len(target_ids) > 0:
                sent.append(t)
                sents.append({
                    'speaker':speaker, 
                    'target_ids':target_ids, 'target_types':target_types,
                    'president':president, 'reporter':reporter,
                    'text': ' '.join(sent)
                })
            target_ids = []
            target_types = []
            sent = []
            
        elif not t.startswith('<') and t.strip() != '':
            sent.append(t)
    
    return sents

def parse_files(paths, method='ut'):
    uts = []
    for path in paths:
        for i, ut in enumerate(parse_tsv(path.read_text(encoding='utf-8'))):
            if method == 'ut':
                uts.append((path.stem, i, parse_ut(ut)))
            elif method == 'sent':
                uts.extend([{'pv':path.stem, 'ut_id':i, **sent} for sent in parse_sent(ut)])
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