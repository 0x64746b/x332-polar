from glob import glob
from csv import reader, DictReader
import pandas as pd
import json

for csv in glob('data/*.csv'):
    print(csv)
    with open(csv) as csv_file:
        x332s = pd.read_csv(csv, delimiter=';').drop(0)
        if x332s.shape != (24, 9):
            print(f'{csv} has an unexpected structure: {x332s.shape}')
        #csv_reader = reader(csv_file, delimiter=';')
        #csv_reader = DictReader(csv_file, delimiter=';')
        #for row in csv_reader:
        #    print(row)

with open('data/orc_2024.valid.json') as all_data:
    x332s = [entry for entry in json.load(all_data) if entry['boat']['type'] == 'X-332']
    print(json.dumps(x332s, indent=4))