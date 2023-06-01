import argparse
from pathlib import Path
import bs4
from utils import parse_inputs, parse_output

TEMPLATE_PATH = [Path('template.xml')]
OUTPUT_PATH = [Path('templated')]

def process(input_path, output_path, template_path):
    template = bs4.BeautifulSoup(template_path.read_text(encoding='utf-8'), features='xml')
    xml_input = bs4.BeautifulSoup(input_path.read_text(encoding='utf-8'), features='xml')

    input_session_title = xml_input.find('title').text.strip()
    input_proofreader_name = xml_input.find('meta', attrs={'name':'relecteur'}).attrs['content'].strip()

    subtitle = template.find('title', attrs={'type':'sub'})
    subtitle.insert(0, input_session_title)

    proofreader_name = template.findAll('respStmt')[6].find('name')
    proofreader_name.insert(0, input_proofreader_name)

    session_coresp = template.find('div1', attrs={'type':'seance'})
    session_coresp.attrs['corresp'] = input_session_title

    session_title = session_coresp.find('title')
    session_title.insert(0, input_session_title)

    (output_path / input_path.name).write_text(template.prettify(formatter=bs4.formatter.XMLFormatter()), encoding='utf-8')


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