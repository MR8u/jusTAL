from src.utils import read_jsonl
import pandas as pd

INPUT = 'data/82_en_core_web_trf_corrected.jsonl'
PERSON_LABEL = 'PERSON'

docs = read_jsonl(INPUT)

rows = []
for i, doc in enumerate(docs):
    for j, ent in enumerate(filter(lambda x: x['label'] == 'PERSON', doc['ents'])):
        start, end = ent['start'], ent['end']
        rows.append((
            i,
            doc['text'].strip(),
            start,
            end,
            doc['text'][start:end],
            j in doc['speakers'],
            j in doc['targets']
        ))
pd.DataFrame(
    rows,
    columns=['sent_id', 'sent_text', 'mention_start', 'mention_end', 'mention_text', 'is_speaker', 'is_target']
).to_csv('data/82_speaker_target.csv', index=False)