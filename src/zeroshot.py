from collections import defaultdict
from pathlib import Path

import bs4
from tqdm import tqdm
from transformers import pipeline

from src.uts import *
from src.utils import write_jsonl 

MODEL_NAME = "BaptisteDoyen/camembert-base-xnli"
OUTPUT_PATH = "data/zeroshot/camembert-base-xnli_1.jsonl"

uts = parse_files(list(Path('data/corrected/').glob('*.tsv')))
candidate_labels = ["est d'accord avec", "n'est pas d'accord avec", "est neutre avec", 'remercie']
hypothesis_template = "Le locuteur {{}} {target}"

docs = []

for pv, i, ut in uts:
    ut = bs4.BeautifulSoup(ut, features='xml')

    speaker = ut.find('u').attrs['who']
    president, reporter = get_president_reporter(ut)
    
    targets = defaultdict(list)
    for target in ut.find_all(lambda x: x.name=='span' and 'ana' in x.attrs):
        targets[target.attrs['ana']].append(target.attrs['type'])

    for target_id, target_types in targets.items():

        hypothesis = hypothesis_template.format(
            speaker=parse_name(speaker, president, reporter), 
            target=parse_name(target_id, president, reporter)
        )

        docs.append({
            'pv':pv,
            'ut_id':i,
            'speaker':speaker,
            'target':target_id,
            'gold':target_types,
            'context':ut.text.strip(),
            'hypothesis':hypothesis,
            'candidates':candidate_labels,
        })


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

write_jsonl(OUTPUT_PATH, docs, encoding='utf-8')

# sequence = "Sur la demande d' avis ,  Monsieur VEDEL  est en plein accord avec la rédaction proposée mais il tient à indiquer au  rapporteur  qu' il ne partage pas son opinion quant au fond de la question . Il estime , d' ailleurs , que la transaction devrait être traitée de la même façon que l' interprêtation qui lie l' administration fiscale . Dans un cas comme dans l' autre , on écarte l' application du droit strict tel qu' il est posé de façon générale par la loi . La question traitée par l' article 1649 quinquies E n' est qu' un raccourci qui aboutit d' ailleurs à une solution équitable puisqu' il permet d' éviter de longues procédures qui aboutiraient au même résultat . Chacun sait qu' il est de jurisprudence constante au Conseil d' Etat , quand 1'administration a , par des renseignements inexacts , porté préjudice à l' administré , qu' elle l' indemnise . En ce qui concer la T.V.A. , ajoutons , d' ailleurs , que si celle-ci est réclamée avec quelques années de retard à la personne qui était chargée de la récupérer on ne voit pas sur qui il lui serait alors possible de le faire . Ceci étant dit , Monsieur VEDEL est en plein accord avec la réponse donnée par le projet de décision ."

# candidate_labels = ["est d'accord avec", "n'est pas d'accord avec", "est neutre avec", 'remercie']
# hypothesis_template = "Monsieur VEDEL {} le rapporteur Segalat"    

# candidate_labels = ["soutient", "rejette", "note"]
# hypothesis_template = "Monsieur VEDEL {} les arguments du rapporteur le rapporteur Segalat" 



# candidate_labels = ["soutient", "s'oppose à", "est indifférent à"]
# hypothesis_template = "Monsieur VEDEL {} la déclaration du rapporteur le rapporteur Segalat"    

# candidate_labels = ["soutient", "s'oppose a"]
# hypothesis_template = "Monsieur VEDEL {} l'arguments du rapporteur le rapporteur Segalat"    

# print(classifier(sequence, candidate_labels, hypothesis_template=hypothesis_template))

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# nli_model = AutoModelForSequenceClassification.from_pretrained("BaptisteDoyen/camembert-base-xnli")
# tokenizer = AutoTokenizer.from_pretrained("BaptisteDoyen/camembert-base-xnli") 
# # sequences
# premise = "Sur la demande d' avis ,  Monsieur VEDEL  est en plein accord avec la rédaction proposée mais il tient à indiquer au  rapporteur  qu' il ne partage pas son opinion quant au fond de la question . Il estime , d' ailleurs , que la transaction devrait être traitée de la même façon que l' interprêtation qui lie l' administration fiscale . Dans un cas comme dans l' autre , on écarte l' application du droit strict tel qu' il est posé de façon générale par la loi . La question traitée par l' article 1649 quinquies E n' est qu' un raccourci qui aboutit d' ailleurs à une solution équitable puisqu' il permet d' éviter de longues procédures qui aboutiraient au même résultat . Chacun sait qu' il est de jurisprudence constante au Conseil d' Etat , quand 1'administration a , par des renseignements inexacts , porté préjudice à l' administré , qu' elle l' indemnise . En ce qui concer la T.V.A. , ajoutons , d' ailleurs , que si celle-ci est réclamée avec quelques années de retard à la personne qui était chargée de la récupérer on ne voit pas sur qui il lui serait alors possible de le faire . Ceci étant dit , Monsieur VEDEL est en plein accord avec la réponse donnée par le projet de décision ."
# hypothesis = "Monsieur VEDEL est neutre avec le rapporteur Segalat ?"

# # tokenize and run through model
# x = tokenizer.encode(premise, hypothesis, return_tensors='pt')
# logits = nli_model(x)[0]
# # we throw away "neutral" (dim 1) and take the probability of
# # "entailment" (0) as the probability of the label being true 
# entail_contradiction_logits = logits[:,::2]
# probs = entail_contradiction_logits.softmax(dim=1)
# prob_label_is_true = probs[:,0]
# print(prob_label_is_true[0].tolist() * 100)
