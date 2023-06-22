from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

PE_PATTERN = re.compile(r"principe d(e l)?'[ée]galit[ée]", re.I)

def normalize_text(text):
    text = text.replace('”', '"')
    text = text.replace("’", "'")
    text = re.sub(r'([A-Za-z])- ([A-Za-z])', r'\1\2', text)
    text = re.sub(r'([^>])\n+\s*', r'\1 ', text)
    return text

def get_pe_paragraphs(paths):
    paragraphs = []

    for path in paths:
        soup = BeautifulSoup(normalize_text(path.read_text(encoding='utf-8')), features='xml')
        for p in soup.find_all('p'):
            paragraphs.append((path.stem, p.text.strip()))

    paragraphs = pd.DataFrame(paragraphs, columns=['fname', 'text'])
    paragraphs['is_pe'] = paragraphs['text'].apply(lambda x: True if PE_PATTERN.search(x) else False)
    paragraphs['year'] = paragraphs['fname'].apply(lambda x: x[2:6])

    return paragraphs

def parse_inputs(inputs):
    paths = []
    for input in inputs:
        input = Path(input)

        if input.is_dir():
            paths.extend(input.glob('*.xml'))
        elif input.suffix == '.xml':
            paths.append(input)
    return paths

def parse_output(output):
    path = Path(output)
    if path.is_dir() == False:
        path.mkdir()
    return path

def read_jsonl(path, encoding='utf-8'):
    """
        Shortcut for read jsonl file

        Parameters
        ----------
        path : str or Path, path of file to read.
        encoding : str, default='utf-8', encoding format to use.
    """
    path = Path(path) if isinstance(path, str) else path
    return [json.loads(line) for line in path.read_text(encoding=encoding).strip().split('\n')]

def write_jsonl(path, data, encoding='utf-8'):
    """
        Shortcut for write jsonl file

        Parameters
        ----------
        path : str or Path, path of file to write.
        data : List, list of json data to write.
        encoding : str, default='utf-8', encoding format to use.
    """
    path = Path(path) if isinstance(path, str) else path
    path.write_text('\n'.join([json.dumps(item) for item in data]), encoding=encoding)