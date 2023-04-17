from functools import reduce
from pathlib import Path
from bs4 import BeautifulSoup
import spacy
from tqdm import tqdm
from src.utils import write_jsonl

INPUT = Path('data/filled/')
MODEL = 'en_core_web_trf'
OUTPUT = Path(f'data/82_{MODEL}.jsonl')

nlp = spacy.load(MODEL)

docs = []

for path in tqdm(list(INPUT.glob('*.xml'))):
    doc = BeautifulSoup(path.read_text(encoding='utf-8'), features="xml").findAll('u')
    doc = reduce(lambda a, b: a + [(i, b.attrs['who'], t.text) for i, t in enumerate(b.findAll('seg'))], doc, [])
    for seg_id, speaker_name, seg_text in doc:
        docs.extend([{'file_name':path.stem, 'speaker_name':speaker_name, 'seg_id':seg_id, 'sent_id':i} | sent.as_doc().to_json() for i, sent in enumerate(nlp(seg_text).sents)])
    write_jsonl(OUTPUT, docs)