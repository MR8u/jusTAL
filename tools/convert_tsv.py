import argparse
import bs4
from pathlib import Path
import spacy
import re

from tools.utils import parse_inputs, parse_output
from tools.fill_template import extract_name_ids, extract_reporter

OUTPUT_PATH = Path('data/tsv/')

nlp = spacy.load("fr_core_news_sm")

def tokenize_xml(root):
    tokens = []
    tokenize_element(root, tokens)
    return tokens

def tag_to_string(tag):
    attrs = ''
    if len(tag.attrs) > 0:
        attrs = ' ' + ' '.join([f'{k}="{v}"' for k, v in tag.attrs.items()])
    return f"<{tag.name}{attrs}>", f"</{tag.name}>"

def tokenize_element(tag, tokens):
    if isinstance(tag, bs4.element.Tag):
        start, end = tag_to_string(tag)
        tokens.append(start)
        for child in tag.children:
            tokenize_element(child, tokens)
        tokens.append(end)
    elif isinstance(tag, bs4.NavigableString):
        tokens.extend([el.text for el in nlp(tag.text.strip())])
    else:
        raise TypeError(f"Unrecognize type: {tag} ({type(tag)}) when parsing xml")

def tokenize_uts(path):
    xml = bs4.BeautifulSoup(path.read_text(encoding='utf-8'), features='xml')
    president = list(filter(lambda x: len(x) == 2, extract_name_ids(xml).values()))[0]
    tokens = []
    for disc in xml.find_all(attrs={'type':'discussion'}):
        reporter = extract_reporter(disc)
        for ut in disc.find_all('u'):
            tokens.append([f'<!-- {president} {reporter} -->'] + tokenize_element(ut))
    return tokens

def convert(input_path, output_path):

    tab = []
    tokens = tokenize_uts(input_path)
    len_words = -1

    for m, tokens in enumerate(tokens):
        tab.append(f'\r#Text={" ".join(tokens)}')
        cur_speaker = '_'
        for n, token in enumerate(tokens):
            # print(f'{m+1}-{n+1}\t{i}-{i+len(token)}\t{token}')
            value_ner = relation = spk_trgt = '_'
            if re.search('<u who=', token):
                # print(re.findall('who="#(.*?)"', token))
                value_ner = 'SPEAKER'
                cur_speaker = f'{m+1}-{n+1}'
            if re.search('<span ana', token):
                # print(re.findall('ana="#(.*?)"', token))
                value_ner = 'TARGET'
                relation = 'NULL'
                spk_trgt = cur_speaker
            tab.append(f'{m+1}-{n+1}\t{len_words+1}-{len_words+len(token)+1}\t{token}\t{str(value_ner)}\t{relation}\t{spk_trgt}')
            len_words+=len(token)+1
    
    tab = [
        '#FORMAT=WebAnno TSV 3.3', 
        '#T_SP=webanno.custom.JusTALNER|value_ner', 
        '#T_RL=webanno.custom.JusTALREL|value_rel|BT_webanno.custom.JusTALNER\r'
        ] + tab

    output_path.write_text('\r'.join(tab), encoding='utf-8')

def get_cli_args() -> argparse.Namespace:
    """Get command line arguments"""
    
    parser = argparse.ArgumentParser(description="Convert xml to tsv")
    parser.add_argument(
        '--inputs', type=str, nargs='+', 
        help='List of file/folder paths to process')
    parser.add_argument(
        '--output', type=str, nargs=1, default=OUTPUT_PATH,
        help=f'(Optional) Output dir to use when saving results. Default = "{OUTPUT_PATH}"')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_cli_args()

    input_path = parse_inputs(args.inputs)
    output_path = parse_output(args.output)

    for input_path in input_path:
        if output_path.is_dir():
            convert(input_path, output_path / f'{input_path.stem}.tsv')
        else:
            convert(input_path, output_path)