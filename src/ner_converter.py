from pathlib import Path

from spacy.tokens.doc import Doc
import spacy

from src.utils import read_jsonl

INPUT = Path("data/82_en_core_web_trf.jsonl")
OUTPUT = Path("data/82_en_core_web_trf.tsv")
MODEL = 'en_core_web_trf'

# def format_ent(t):
    # return '_' if t == '' else f'{t}[{ENT_TYPE_COUNTS[t]}]'

nlp = spacy.load(MODEL)

lines = [
    "#FORMAT=WebAnno TSV 3.3",
    "#T_SP=webanno.custom.JusTALNER|isSpeaker|isTarget|value",
    "\n",
]

docs = read_jsonl(INPUT)

i = 1
k = 0
c = 0

for i, doc in enumerate(docs):
    doc = Doc(nlp.vocab).from_json(doc)
    text = doc.text
    lines.append(f"#Text={text.strip()}")
    for j, token in enumerate(doc):
        start, end = token.idx, token.idx + len(token)
        isSpeaker, isTarget, ent  = '_', '_', '_'
        if token.ent_iob_ == 'B' :
            if doc[j+1].ent_iob_ == 'I':
                k+=1
                isSpeaker = f'false[{k}]'
                isTarget = f'false[{k}]'
                ent = f'{token.ent_type_}[{k}]'
            else:
                isSpeaker = f'false'
                isTarget = f'false'
                ent = f'{token.ent_type_}'
        elif token.ent_iob_ == 'I':
            isSpeaker = f'false[{k}]'
            isTarget = f'false[{k}]'
            ent = f'{token.ent_type_}[{k}]'
        lines.append(f'{i+1}-{j+1}\t{c+start}-{c+end}\t{text[start:end]}\t{isSpeaker}\t{isTarget}\t{ent}')
    lines[-1] += '\n'
    c += end
    
OUTPUT.write_text("\n".join(lines), encoding='utf-8')