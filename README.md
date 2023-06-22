# jusTAL

Github repository: https://github.com/MR8u/jusTAL

Not all code is well commented and documented. We will improve this in the next few days.

Install required library with:

```
pip install -r requirements.txt
```

## Tools

### fill_template

The program used to process structured xml files.

```
usage: fill_template.py [-h] [--inputs INPUTS [INPUTS ...]] [--output OUTPUT] [--template TEMPLATE]

Fill Tempalte

optional arguments:
  -h, --help            show this help message and exit
  --inputs INPUTS [INPUTS ...]
                        List of file/folder paths to process
  --output OUTPUT       (Optional) Output dir to use when saving results. Default = "[WindowsPath('data/templated')]"     
  --template TEMPLATE   (Optional) Template file path to use. Default = "[WindowsPath('data/template.xml')]"
```

### convert_tsv

The program used to extract utterances and convert them to tsv for annotation.

```
usage: convert_tsv.py [-h] [--inputs INPUTS [INPUTS ...]] [--output OUTPUT]

Convert xml to tsv

optional arguments:
  -h, --help            show this help message and exit
  --inputs INPUTS [INPUTS ...]
                        List of file/folder paths to process
  --output OUTPUT       (Optional) Output dir to use when saving results. Default = "data\tsv"
```

## src

All this file are not CLI ready. Parameters are, most of the time, in top the file.

  - utils.py : Contains various functions used throughout the project.
  - uts.py : Contains functions to process utterances from tsv files to the differents models.
  - zeroshot.py : The program used to test NLI models.
  - sentiment.py : The program used to test sentiment analysis models.
  - fewshot.py : The program used to finetune NLI models on few examples.

## data

  - corrected : Contains manually structured xml files.
  - templated : Contains xml files after being processed by fill_template.
  - tsv : Annotated utterances in tsv format.
  - zeroshot : Some results of NLI models on tsv files.
  - template.xml : Template used by fill_template.

## notebooks

  - discussion_application.ipynb : All our work on speaker target relation analysis"application". Including visualation as graph.
  - egalite_distrib.ipynb : Work on egalite distribution.
  - egalite_pos.ipynb : Work on egalite POS and dependencies.
  - zeroshot_ana.ipynb : Analysis of results of NLI models.
