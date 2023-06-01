import re

def is_president(x):
    return re.search(r'pr[ée]sident', x['mention_text'], re.I)

def is_rapporteur(file_names):   
    def wrapped_is_rapporteur(x):
        return x['decision_id'] in file_names and re.search(r'rapporteur', x['mention_text'], re.I)
    return wrapped_is_rapporteur

PERSONS = {
    'frey':[is_president],
    'vedel':[is_rapporteur(['#DC-82-139', '#DC-82-142', '#DC-82-144', '#DC-82-145'])],
    'segalat':[is_rapporteur(['#DC-82-140', '#DC-82-143', '#L-82-129', '#DC-82-154'])],
    'gros':[is_rapporteur(['#DC-82-141', '#DC-82-146'])],
    'lecourt':[is_rapporteur(['#DC-82-137', '#DC-81-134', '#L-82-127'])],
    'monnerville':[],
    'brouillet':[],
    'peretti':[is_rapporteur(['#L-82-128'])],
    'joxe':[],
    'giscard':[]
}

def match_person(x):
    for k, v in PERSONS.items():
        if re.search(f'{k}', x['mention_text'], re.I):
            return k
        for func in v:
            if func(x):
                return k
    return ''