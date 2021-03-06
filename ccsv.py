import csv
import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).parent)
import parse_tools as ptools

def compute_ccsv(fpath):
    '''
    Compute and output a single ccsv file

    Inputs:
        - fpath (str or Path)
    '''
    csv_lines, tags = ptools.file_splitter(fpath)
    computed_lines = ptools.compute_lines(csv_lines)

    new_path = Path(fpath).resolve().with_suffix('.csv')

    with open(new_path, 'w', encoding='utf-8') as wfile:
        writer = csv.writer(wfile)
        writer.writerows(computed_lines)

    print(f"Created file at {fpath}")


@click.command()
@click.argument('infiles', nargs=-1, type=click.Path(exists=True))
@click.option('-f', '--force', is_flag=True, default=False)
def main(infiles, force):
    '''
    Compute a list of .ccsv file. For each file in INFILES, compute and output <filename>.ccsv -> <filename>.csv
    '''
    import pdb;pdb.set_trace()

    for fpath in infiles:
        compute_ccsv(fpath)



if __name__ == '__main__':
    main()