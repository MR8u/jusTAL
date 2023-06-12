import argparse
from pathlib import Path
import bs4
from tools.utils import parse_inputs, parse_output
from src.postprocess import PERSONS
import re
import datetime
from functools import reduce
from xml.dom import minidom

TEMPLATE_PATH = [Path('template.xml')]
OUTPUT_PATH = Path('templated')
VALID_TYPES = ['discussion']
TEXT_TAGS = ['writing','u']

HEADER_PATTERN = re.compile(r'h[0-9]')

    # + Remplacer les ” -> " et ’ -> ' problèmatique
    # + Remplace [A-Za-z]- [A-Za-z] -> [A-Za-z][A-Za-z]
def normalize_text(text):
    text = text.replace('”', '"')
    text = text.replace("’", "'")
    text = re.sub(r'([A-Za-z])- ([A-Za-z])', r'\1\2', text)
    text = re.sub(r'([^>])\n+\s*', r'\1 ', text)
    return text

def process_div1(input, output):
    input_div1 = input.find('div1')
    assert input_div1 and "type" in input_div1.attrs and input_div1.attrs['type']=='pv', f'{input_path} has no <div1> of @type "pv"'
    assert 'corresp' in input_div1.attrs and input_div1.attrs['corresp'][0]=='#' and output.find('category', attrs={'xml:id':input_div1.attrs['corresp'][1:]}), f'{input_path} has no <div1> with valid @corresp'
    output.find('body').insert(0, input_div1)

def process_back(input, output):
    input_back = input.find('back')
    output.find('text').append(input_back)

def process_underline(output):
    for u in output.find_all('u'):
        if 'who' not in u.attrs:
            rewrite_u(u)

def rewrite_u(u):
    u.name = 'hi'
    u.attrs['rend'] = 'underline'

def parse_date(text):
    return datetime.datetime(int(text[0:4]), int(text[5:7]), int(text[8:10]))

def extract_name_ids(template):
    date_pv = template.find('div1').attrs['corresp']
    date_pv = parse_date(date_pv[3:])
    name_ids = {"#all":[], "#default":[]}
    for person in template.find('profileDesc').find_all('person'):
        for affiliation in person.find_all('affiliation'):
            from_date, to_date = parse_date(affiliation['from']), parse_date(affiliation['to']) if 'to' in affiliation.attrs else datetime.datetime.now()
            if from_date > date_pv or to_date < date_pv:
                continue
            k ='#' + person.attrs['xml:id']
            name_ids[k] = [f'({person.surname.text})\W']
            if affiliation['role']=='president':
                name_ids[k].append("(pr[ée]sident)\W(?!d[eu'])")
    return name_ids

def extract_reporter(tag):
    tag = [t for t in tag.parents if 'type' in t.attrs and t.attrs['type'] == 'question']
    if len(tag) == 0:
        return ''
    tag = tag[0]

    tag = tag.find(attrs={'type':'rapport'})
    if not tag:
        return ''
    
    tag = tag.find(lambda x: 'who' in x.attrs)
    if not tag:
        return ''
    
    return tag.attrs['who']

def match_person(x, name_ids):
    for k, v in name_ids.items():
        for r in v:
            if re.search(r, x, re.I):
                return k
    return ''

def match_persons(x, name_ids):
    persons = []
    for k, v in name_ids.items():
        for r in v:
            for m in re.findall(r, x, re.I):
                persons.append((m,k))
    return persons

def process_who(output):
    names_ids = extract_name_ids(output)
    for tag in output.find('text').find_all(lambda x: 'who' in x.attrs):
        ids = []
        for i in tag.attrs['who'].split(' '):
            # TODO: Raise error/warning when match_person return ''
            ids.append(i if i in names_ids.keys() else match_person(i + ' ', names_ids))
        tag.attrs['who'] = ' '.join(ids)

def match_speaker(a, b):
    return set(a.split(' ')) == set(b.split(' '))

def process_speaker(output):
    # current_speaker = match_person('president', names_ids)
    # TODO : Refactor 
    for tag in output.find_all(lambda x: 'type' in x.attrs and x.attrs['type'] in VALID_TYPES):

        names_ids = extract_name_ids(output)
        reporter = extract_reporter(tag)
        if reporter:
            names_ids[reporter].append('(rapporteur)\W')

        current_speaker = '#default'

        for p in tag.find_all('p'):
            if p.parent.name in TEXT_TAGS:
                if 'who' in p.parent.attrs.keys():
                    current_speaker = p.parent.attrs['who']
            else:
                u = p.find('u')
                if u:
                    tmp = match_person(u.text, names_ids)
                    current_speaker = tmp if tmp else current_speaker
                    rewrite_u(u)
                
                utterances = [ut for ut in p.previous_siblings]
                utterances = [ut for ut in utterances if isinstance(ut, bs4.element.Tag) and 'who' in ut.attrs]
                # print(current_speaker, [ut.attrs for ut in utterances])
                if len(utterances) > 0 and match_speaker(utterances[0].attrs['who'], current_speaker):
                    utterances[0].append(p)
                else:
                    u = output.new_tag('u', attrs={'who':current_speaker})
                    p.insert_before(u)
                    u.append(p)

def process_targets(output):
    for tag in output.find_all(lambda x: 'type' in x.attrs and x.attrs['type'] in VALID_TYPES):

        names_ids = extract_name_ids(output)
        reporter = extract_reporter(tag)
        if reporter:
            names_ids[reporter].append('(rapporteur)\W')
        
        for p in tag.find_all('p'):
            txt = str(p)
            for m, t in match_persons(txt, names_ids):
                if t in p.parent.attrs['who'].split(' '):
                    txt = txt.replace(m, f'<span ana="{t}">{m}</span>')
            p.replace_with(bs4.BeautifulSoup(txt, features="lxml").find('p'))

        while True:
            sp = output.find(lambda x: x.name=='span' and x.parent.name=='span' and 'ana' in x.attrs)
            if not sp:
                break
            sp.replace_with(sp.string)
                
def rewrite_all_p(output):  
    for tag in output.find_all(lambda x: x.name in TEXT_TAGS):
        for p in tag.find_all('p'):
            p.name = 'seg'

def process_headers(output):
    for h in output.find_all(lambda x: HEADER_PATTERN.match(x.name)):
        style = f'titre{h.name[1]}'
        h.name = 'hi'
        h.attrs['style'] = style

def format_xml(output):
    return output.prettify(formatter=bs4.formatter.XMLFormatter())

def process(input_path, output_path, template_path):
    template = bs4.BeautifulSoup(normalize_text(template_path.read_text(encoding='utf-8')), features='xml')
    xml_input = bs4.BeautifulSoup(normalize_text(input_path.read_text(encoding='utf-8')), features='xml')
    #handle proofreader
    input_proofreader_name = xml_input.find('meta', attrs={'name':'relecteur'}).attrs['content'].strip()
    proofreader_name = template.findAll('respStmt')[6].find('name')
    proofreader_name.insert(0, input_proofreader_name)

    process_div1(xml_input, template)
    process_back(xml_input, template)

    process_who(template)
    process_speaker(template)
    process_targets(template)
    process_headers(template)
    # underline should be process after speaker.
    process_underline(template)
    rewrite_all_p(template)
    
    (output_path / input_path.name).write_text(format_xml(template), encoding='utf-8')

def get_cli_args() -> argparse.Namespace:
    """Get command line arguments"""
    
    parser = argparse.ArgumentParser(description="Fill Tempalte")
    parser.add_argument(
        '--inputs', type=str, nargs='+', 
        help='List of file/folder paths to process')
    parser.add_argument(
        '--output', type=str, nargs=1, default=OUTPUT_PATH,
        help=f'(Optional) Output dir to use when saving results. Default = "{OUTPUT_PATH}"')
    parser.add_argument(
        '--template', type=str, nargs=1, default=TEMPLATE_PATH, 
        help=f'(Optional) Template file path to use. Default = "{TEMPLATE_PATH}"')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_cli_args()

    output_path = parse_output(args.output)

    template_path = Path(args.template[0])

    for input_path in parse_inputs(args.inputs):
        process(input_path, output_path, template_path)