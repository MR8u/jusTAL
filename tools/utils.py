from pathlib import Path

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
