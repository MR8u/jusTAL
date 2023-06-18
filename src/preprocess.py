from pathlib import Path
import re

from bs4 import BeautifulSoup
import pandas as pd

from tools.fill_template import normalize_text

PE_PATTERN = re.compile(r"principe d('|e l')[eé]galit[eé]", re.I)

def get_pe_paragraphs(path):
    paragraphs = []

    for path in list(path.glob('*.xml')):
        soup = BeautifulSoup(normalize_text(path.read_text(encoding='utf-8')), features='xml')
        for p in soup.find_all('p'):
            paragraphs.append((path.stem, p.text.strip()))

    paragraphs = pd.DataFrame(paragraphs, columns=['fname', 'text'])
    paragraphs['is_pe'] = paragraphs['text'].apply(lambda x: True if PE_PATTERN.search(x) else False)
    paragraphs['year'] = paragraphs['fname'].apply(lambda x: x[2:6])

    return paragraphs