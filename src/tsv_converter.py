import random
from tqdm import tqdm
from src.utils import read_jsonl, write_jsonl
from pathlib import Path

from spacy.tokens.doc import Doc
from spacy.tokens import DocBin
import spacy
import re

SOURCE_PATH = 'data/82_en_core_web_trf.jsonl'
CORRECTED_PATH = 'data/82_en_core_web_trf_corrected.tsv'
MODEL = 'en_core_web_trf'
ENT_PATTERN = re.compile('([^[]+)(?:\[([0-9]+)\])?')
LABELS = ['PERSON', 'ORG', 'LAW', 'GPE', 'LOC', 'DATE', 'TIME']

docs = read_jsonl(SOURCE_PATH)
lines = Path(CORRECTED_PATH).read_text(encoding='utf-8').splitlines()
if lines[-1] != '':
    lines.append('')

nlp = spacy.load(MODEL)
nlp.disable_pipes(['tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner'])

i = 0
doc, ents, last_ent_id = None, None, None
for l in tqdm(lines, 'Process lines:'):
    if l.startswith('#Text'):
        doc = docs[i]
        ents = []
        speakers = []
        targets = []
        i += 1

    elif l.startswith(str(i)):
        splitted = l.strip().split('\t')
        if len(splitted) == 6:
            token_idx, sent_idx, token_text, speaker, target, ent = splitted
        else:
            token_idx, sent_idx = splitted[:2]
            token_text = '\t'.join(splitted[2:2+len(splitted)-5])
            speaker, target, ent = splitted[2+len(splitted)-5:]

        token = doc['tokens'][int(token_idx.split('-')[-1]) - 1]

        if ent != '_':
            ent_type, ent_id = ENT_PATTERN.match(ent).groups()
            if ent_id == None or ent_id != last_ent_id:
                if speaker.startswith('true'):
                    speakers.append(len(ents))
                if target.startswith('true'):
                    targets.append(len(ents))
                ents.append({'start':token['start'], 'end':token['end'], 'label':ent_type})
                last_ent_id = ent_id
            elif last_ent_id == ent_id:
                ents[-1]['end'] = token['end']               
    elif l == '' and doc != None:
        doc['ents'] = list(filter(lambda x: x['label'] in LABELS, ents))
        doc['speakers'] = speakers
        doc['targets'] = targets

print(lines[-1])

write_jsonl('data/82_en_core_web_trf_corrected.jsonl', docs)

# Full

# db = DocBin()
# for doc in tqdm(docs, 'Process full docs:'):
#     db.add(Doc(nlp.vocab).from_json(doc))
# db.to_disk("./82_full.spacy")

# # Train, Test, Dev

# def get_splits_size(n):
#     x = int(n * .7)
#     x -= (n - x) % 2
#     y = int((n - x) / 2)
#     return x, y, y

# train_size, dev_size, test_size = get_splits_size(len(docs))
# print(train_size, dev_size, test_size)

# random.seed(42)
# random.shuffle(docs)

# db = DocBin()
# for doc in tqdm(docs[:train_size], 'Process train docs:'):
#     db.add(Doc(nlp.vocab).from_json(doc))
# assert len(db) == train_size, f'Train size is wrong : {len(db)} != {train_size}'
# db.to_disk("data/82_train.spacy")

# db = DocBin()
# for doc in tqdm(docs[train_size:train_size+dev_size], 'Process dev docs:'):
#     db.add(Doc(nlp.vocab).from_json(doc))
# assert len(db) == dev_size, f'Dev size is wrong : {len(db)} != {dev_size}'
# db.to_disk("data/82_dev.spacy")

# db = DocBin()
# for doc in tqdm(docs[train_size+dev_size:], 'Process test docs:'):
#     db.add(Doc(nlp.vocab).from_json(doc))
# assert len(db) == test_size, f'Test size is wrong : {len(db)} != {test_size}'
# db.to_disk("data/82_test.spacy")

