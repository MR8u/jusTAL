from collections import defaultdict
from pathlib import Path
import random
import re

import bs4
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from src.uts import *
from src.utils import write_jsonl 

MODEL_NAME = "BaptisteDoyen/camembert-base-xnli"
# MODEL_NAME = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
USE_NAME = False
SEGMENTATION = 'chunk'

TID = 'h_semble'

# TEMPLATES = {
#     'h0':{
#         'hypothesis_template': "Le locuteur ({speaker}) argumente avec {target}",
#         'candidate_labels': []
#     },
#     'h1':{
#         'hypothesis_template': "Le locuteur ({speaker}) débat avec {target}",
#         'candidate_labels': []
#     },
#     'h2':{
#         'hypothesis_template': "Le locuteur ({speaker}) est d'accord avec {target}",
#         'candidate_labels': []
#     },
#     'h3':{
#         'hypothesis_template': "Le locuteur ({speaker}) n'est pas d'accord avec {target}",
#         'candidate_labels': []
#     },
#     'h4':{
#         'hypothesis_template': "Accord avec {target}",
#         'candidate_labels': []
#     },
#     'h4b':{
#         'hypothesis_template': "Le locuteur est d'accord avec {target}",
#         'candidate_labels': []
#     },
#     'h5':{
#         'hypothesis_template': "Désaccord avec {target}",
#         'candidate_labels': []
#     },
#     'h6':{
#         'hypothesis_template': "Soutient avec {target}",
#         'candidate_labels': []
#     },
#     },
#     'an':{
#         'hypothesis_template': "La phrase est une antiphrase",
#         'candidate_labels': []
#     },
#     'anb':{
#         'hypothesis_template': "Exprime une phrase positive, mais sous-entends son contraire",
#         'candidate_labels': []
#     },
#     'anc':{
#         'hypothesis_template': "Est partiellement d'accord avec {target}",
#         'candidate_labels': []
#     },
#     'c0': {
#         'hypothesis_template': "Le locuteur {{}} {target}",
#         'candidate_labels': ["est d'accord avec", "n'est pas d'accord avec", "est neutre avec", 'remercie'],
#     },
#     'c1': {
#         'hypothesis_template': "Le locuteur {{}} {target}",
#         'candidate_labels': ["est d'accord avec", "n'est pas d'accord avec", "est neutre avec", 'remercie', 'donne la parole'],
#     }
# }

TEMPLATES = {
    'h_est':{
        'hypothesis_template': "Le locuteur est d\'accord avec {target}",
        'candidate_labels': []
    },
    'h_semble':{
        'hypothesis_template': "Le locuteur semble d\'accord avec {target}",
        'candidate_labels': []
    },
    'c_gpt': {
        'hypothesis_template': "Le locuteur {{}} {target}",
        'candidate_labels': [
            "semble d'accord avec", 
            "semble en désaccord avec", 
            "n'a pas exprimé d'opinion claire par rapport a", 
            "semble remercier"
        ],
    },
    'c_semble': {
        'hypothesis_template': "Le locuteur {{}} {target}",
        'candidate_labels': ["semble d'accord avec", "semble en désaccord avec", "semble neutre avec", "semble remercier"],
    },
    'c_est': {
        'hypothesis_template': "Le locuteur {{}} {target}",
        'candidate_labels': ["est d'accord avec", "n'est pas d'accord avec", "est neutre avec", 'remercie'],
    },
    'cc_semble': {
        'hypothesis_template': "Le locuteur {{}} {target}",
        'candidate_labels': ["semble d'accord avec", "semble en désaccord avec"],
    },
    'cc_semble_inverse': {
        'hypothesis_template': "Le locuteur {{}} {target}",
        'candidate_labels': ["semble en désaccord avec", "semble d'accord avec"],
    }
}

NAMES = [
    'Martin',
    'Bernard',
    'Thomas',
    'Petit',
    'Robert',
    'Richard',
    'Durand',
    'Dubois',
    'Moreau',
    'Laurent',
]

OUTPUT_PATH = f"data/zeroshot/{MODEL_NAME.split('/')[-1]}_{TID}_{SEGMENTATION}_{'name' if USE_NAME else ''}.jsonl"

uts = parse_files(list(Path('data/tsv/').glob('*.tsv')), SEGMENTATION)

hypothesis_template = TEMPLATES[TID]['hypothesis_template']
candidate_labels = TEMPLATES[TID]['candidate_labels']

def generate_with_targets(uts):
    docs = []
    for ut in uts:

        for target_id, target_type, target_value in zip(ut['target_ids'], ut['target_types'], ut['target_values']):

            hypothesis = hypothesis_template.format(
                speaker=parse_name(ut['speaker'], ut['president'], ut['reporter']), 
                # target=parse_name(target_id, ut['president'], ut['reporter'])
                target=target_value
            )

            docs.append({
                'pv':ut['pv'],
                'ut_id':ut['ut_id'],
                'speaker':ut['speaker'],
                'target':target_id,
                'gold':[target_type],
                'context':ut['text'],
                'target_value':target_value,
                'hypothesis':hypothesis,
                'candidates':candidate_labels,
            })

    return docs

def generate_with_names(uts):
    docs = []
    
    for ut in uts:
        for target_id, target_type, target_value in zip(ut['target_ids'], ut['target_types'], ut['target_values']):
            random.shuffle(NAMES)
            name = NAMES[0]
            context = ut['text']
            
            if re.search('pr[ée]sident', target_value, re.I) == None and re.search('rapporteur', target_value, re.I) == None:
                context = ut['text'].replace(target_value, name)
                assert context != ut['text']
                target_value = name

            hypothesis = hypothesis_template.format(
                speaker=parse_name(ut['speaker'], ut['president'], ut['reporter']), 
                # target=parse_name(target_id, ut['president'], ut['reporter'])
                target=target_value
            )

            docs.append({
                'pv':ut['pv'],
                'ut_id':ut['ut_id'],
                'speaker':ut['speaker'],
                'target':target_id,
                'gold':[target_type],
                'context':context,
                'hypothesis':hypothesis,
                'candidates':candidate_labels,
            })

    return docs

def custom_classify(docs):
        nli_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) 
        nli_model.eval()

        for doc in tqdm(docs):
            candidate_hypothesis, candidate_scores, candidate_preds = [], [], []
            labels = [len(candidate_labels)]

            for i, candidate in enumerate(candidate_labels):
                ch = doc['hypothesis'].format(candidate)
                candidate_hypothesis.append(ch)
                x = tokenizer.encode(
                     doc['context'], 
                     ch, 
                     truncation='only_first', 
                     return_tensors='pt'
                )
                logits = nli_model(x)[0]

                scores = logits.softmax(dim=1)
                pred = scores.argmax().item()

                candidate_scores.append(scores)
                candidate_preds.append(pred)
                
                if pred == 0:
                    labels = [i]
                    break

            doc.update({
                'labels':labels
            })

def check_hypothesis(docs):
        nli_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) 
        nli_model.eval()


        for doc in tqdm(docs):

            x = tokenizer.encode(doc['context'], doc['hypothesis'], truncation='only_first', return_tensors='pt')
            logits = nli_model(x)[0]
            # print(logits[:,::2], logits)
            scores = logits.softmax(dim=1)

            doc.update({
                'scores':scores.tolist(),
                'labels':[scores.argmax().item()]
            })

def classify(docs):
    classifier = pipeline(
        "zero-shot-classification", 
        model=MODEL_NAME
    )

    for doc in tqdm(docs):
        output = classifier(doc['context'], doc['candidates'], hypothesis_template=doc['hypothesis'])
        doc.update({
            'scores':output['scores'],
            'labels':output['labels']
        })

if USE_NAME:
    docs = generate_with_names(uts)
else:
    docs = generate_with_targets(uts)

check_hypothesis(docs)
# custom_classify(docs)
classify(docs)

write_jsonl(OUTPUT_PATH, docs, encoding='utf-8')