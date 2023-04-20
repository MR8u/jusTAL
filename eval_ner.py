from src.utils import read_jsonl
from nervaluate import Evaluator

GOLD_PATH = 'data/82_en_core_web_trf_corrected.jsonl'
PRED_PATH = 'data/82_en_core_web_trf.jsonl'

LABELS = ['PERSON', 'ORG', 'LAW', 'GPE', 'LOC', 'DATE', 'TIME']

golds = read_jsonl(GOLD_PATH)
preds = read_jsonl(PRED_PATH)

evaluator = Evaluator([gold['ents'] for gold in golds], [pred['ents'] for pred in preds], tags=LABELS)
results, results_per_tag = evaluator.evaluate()
print(results)
print(results_per_tag['PERSON'])

# nlp = spacy.load(MODEL)

    # iobs = []
    # for doc in tqdm(docs):
#     iobs.append([])
#     for token in Doc(nlp.vocab).from_json(doc):
#         iobs[-1].append('O' if token.ent_iob_ == 'O' else f'{token.ent_iob_}-{token.ent_type_}')

