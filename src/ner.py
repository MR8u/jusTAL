from functools import reduce
from pathlib import Path
from bs4 import BeautifulSoup
import spacy
from tqdm import tqdm
from src.utils import write_jsonl

INPUT = Path('data/filled/')
MODEL = 'en_core_web_trf'
OUTPUT = Path(f'data/82_{MODEL}.jsonl')
OUTPUT = Path(f'data/snif.jsonl')   

nlp = spacy.load(MODEL)

docs = []

def get_question_id(u):
    question = u.find_parent('div3', attrs={'type':'question'})
    return question['corresp'] if question and 'corresp' in question.attrs else ''

for path in tqdm(list(INPUT.glob('*.xml'))):
    utterances = BeautifulSoup(path.read_text(encoding='utf-8'), features="xml").findAll('u')
    segs = reduce(lambda a, b: a + [(i, get_question_id(b), b.attrs['who'], t.text) for i, t in enumerate(b.findAll('seg'))], utterances, [])
    for seg_id, qid, speaker_name, seg_text in segs:
        docs.extend([{'file_name':path.stem, 'decision_id':qid, 'speaker_name':speaker_name, 'seg_id':seg_id, 'sent_id':i} | sent.as_doc().to_json() for i, sent in enumerate(nlp(seg_text).sents)])
    write_jsonl(OUTPUT, docs)

print('')