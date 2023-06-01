import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from tools.utils import parse_inputs, parse_output
from bs4 import BeautifulSoup

OUTPUT_PATH = [Path('graphs')]

GROUP_BY = 'decision'
KEEP_SPEAKERS = 'all'
SORT_SPEAKERS = 'asc'

def faire_graph(soupe:BeautifulSoup, output_path):
    df=pd.DataFrame([element for sousliste in [tag['who'].split(' ') for tag in soupe.find_all() if tag.has_attr('who')] for element in sousliste][6:], columns = ['pers'])

    unique_pers = list(df.pers.unique())

    plt.scatter(
        range(1,len(df)+1), 
        df.pers, 
        marker = "o", 
        c=df.pers.apply(lambda x: unique_pers.index(x)).to_list(), 
        cmap='Set1',
        zorder=2
    )

    plt.plot(
        range(1,len(df)+1), 
        df.pers, 
        linewidth=1,
        c='black',
        zorder=1
    )
    
    plt.xticks(range(1,len(df)+1), range(1,len(df)+1))
    plt.title(soupe.find('title', attrs={"type": "sub"}).contents[0].strip())
    plt.xlabel('Interventions')
    plt.ylabel('Conseiller')
    plt.savefig(output_path)

def get_cli_args() -> argparse.Namespace:
    """Get command line arguments"""
    
    parser = argparse.ArgumentParser(description="Build Speaker Time Graph")
    parser.add_argument(
        '--inputs', type=str, nargs='+', 
        help='List of file/folder paths to process')
    parser.add_argument(
        '--output', type=str, nargs=1, default=OUTPUT_PATH,
        help=f'(Optional) Output dir to use when saving results. Default = "{OUTPUT_PATH}"')
    parser.add_argument(
        '--groupby', type=str, nargs=1, default=GROUP_BY,
         help=f'(Optional) Group result by given arg. One graph will be made by group. Default = "{GROUP_BY}". Accepted = ["no", "pv", "seance", "decision"]')
    parser.add_argument(
        '--keep_speakers', type=str, nargs=1, default=KEEP_SPEAKERS,
         help=f'(Optional) Keep or not all the speaker of the corpus for each graph. Default = "{KEEP_SPEAKERS}". Accepted = ["all", "partial"]')
    parser.add_argument(
        '--sort_speakers', type=str, nargs=1, default=SORT_SPEAKERS,
         help=f'(Optional) Sort or not the speakers. Default = "{SORT_SPEAKERS}". Accepted = ["asc", "desc", "no"]')


    return parser.parse_args()

if __name__ == '__main__':
    # args = get_cli_args()

    # output_path = parse_output(args.output)
    # group_by = args.group_by[0]
    # group_by = args.group_by[0]
    # keep_speakers = args.keep_speakers[0]
    # sort_speakers = args.sort_speakers[0]

    # text = ''
    # for input_path in parse_inputs(args.inputs):
    #     text += input_path.read_text()
    
    # soup = BeautifulSoup(text)

    # if group_by == 'all':
    #     faire_graph(soup, output_path / 'speaker_time_graph.png')
    # else:
    #     for tag in soup.findAll(attrs={'type':group_by}):
    #         faire_graph(tag, ou)