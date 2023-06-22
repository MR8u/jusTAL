from tqdm import tqdm
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from pathlib import Path
from src.uts import *
from src.utils import write_jsonl

docs = []

MODEL_NAME = "cmarkea/distilcamembert-base-sentiment"
OUTPUT_PATH = f"data/sentiment/{MODEL_NAME.split('/')[-1]}.jsonl"
uts = parse_files(list(Path('data/tsv/').glob('*.tsv')), 'sent')

for ut in uts:
    for target_id, target_type in zip(ut['target_ids'], ut['target_types']):
        docs.append({
            'pv':ut['pv'],
            'ut_id':ut['ut_id'],
            'speaker':ut['speaker'],
            'target':target_id,
            'gold':[target_type],
            'context':ut['text'],
        })


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

for doc in tqdm(docs):
    output = classifier(doc['context'])[0]
    doc.update({
        'scores':[output['score']],
        'labels':[output['label']]
    })
    
write_jsonl(OUTPUT_PATH, docs, encoding='utf-8')