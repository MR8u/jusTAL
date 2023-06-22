from tqdm import tqdm
from transformers import pipeline, CamembertTokenizer, AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments 
from torch.utils.data import Dataset
from src.utils import read_jsonl, write_jsonl
import random

MODEL_NAME = 'BaptisteDoyen/camembert-base-xnli'
N_EXAMPLE_BY_CLASS = 2

METHOD = 'hyp'

GOLD_TO_PRED = {"POSITIF":0, "NEGATIF":2, "NEUTRAL":1, "CIVILITY":1, 'NULL':1}

HYPOTHESIS_TEMPLATE = "Le locuteur {{}} {target}"
CANDIDATE_LABELS = {
    "POSITIF":"semble d'accord avec", 
    "NEGATIF":"semble en désaccord avec", 
    "NEUTRAL":"semble neutre avec", 
    "CIVILITY":"semble remercier",
}

TEST_OUTPUT_PATH = f"data/zeroshot/justal_fs_h2_semble_chunk.jsonl"

docs = read_jsonl('data/zeroshot/camembert-base-xnli_h_semble_chunk_.jsonl')

data = {'train':[], 'test':[]}

for label in ['POSITIF', 'NEGATIF', 'NEUTRAL', 'CIVILITY']:
    examples = list(filter(lambda x: x['gold'][0] == label, docs))
    random.shuffle(examples)
    data['train'].extend(examples[:N_EXAMPLE_BY_CLASS])
    data['test'].extend(examples[N_EXAMPLE_BY_CLASS:])

data['test'].extend(list(filter(lambda x: x['gold'][0] == 'NULL', docs)))

print(len(data['train']), len(data['test']))

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = CamembertTokenizer.from_pretrained(MODEL_NAME) 

def preprocess_hyp(tokenizer, example):
    inputs = tokenizer(
        example['context'], example['hypothesis'],
        add_special_tokens=True,
        truncation="only_first",
    )
    inputs['label'] = GOLD_TO_PRED[example['gold'][0]]
    return inputs

def preprocess_cls(tokenizer, example):
    candidate = CANDIDATE_LABELS[example['gold'][0]]
    inputs = tokenizer(
        example['context'], HYPOTHESIS_TEMPLATE.format(target=example['target_value']).format(candidate),
        add_special_tokens=True,
        truncation="only_first",
    )
    inputs['label'] = 0
    return inputs

class FSDataset(Dataset):
    def __init__(self, tokenizer, examples, method="hyp"):
        super(FSDataset).__init__()
        self.tokenizer = tokenizer
        self.examples = examples
        if method == "hyp":
            self.preprocess = preprocess_hyp
        elif method == "cls":
            self.preprocess = preprocess_cls

    def __getitem__(self, index):
        return self.preprocess(self.tokenizer, self.examples[index])
    
    def __len__(self):
        return len(self.examples)

# data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="models/justal-fs-cls",
    num_train_epochs=1,
    per_device_train_batch_size=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=FSDataset(tokenizer, data['train'], METHOD),
    # data_collator=data_collator,
)

trainer.train()
trainer.save_model(output_dir=training_args.output_dir)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) 

model.eval()

if METHOD == 'hyp':
    for doc in tqdm(data['test']):
        x = tokenizer.encode(doc['context'], doc['hypothesis'], truncation='only_first', return_tensors='pt').to('cuda:0')
        logits = model(x)[0]
        scores = logits.softmax(dim=1)
        doc.update({
            'scores':scores.tolist(),
            'labels':[scores.argmax().item()]
        })

elif METHOD == 'cls':
    classifier = pipeline(
        "zero-shot-classification", 
        model=model.to('cpu'),
        tokenizer=tokenizer
    )
    
    for doc in tqdm(docs):
        output = classifier(doc['context'], list(CANDIDATE_LABELS.values()), hypothesis_template=HYPOTHESIS_TEMPLATE.format(target=doc['target_value']))
        doc.update({
            'scores':output['scores'],
            'labels':output['labels']
        })

write_jsonl(TEST_OUTPUT_PATH, data['test'], encoding='utf-8')
