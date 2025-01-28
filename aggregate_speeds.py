from collections import defaultdict
from glob import glob
from csv import reader, DictReader
from importlib.metadata import entry_points

import numpy as np
import pandas as pd
import json

from numpy.f2py.crackfortran import entrypattern

#for csv in glob('data/*.csv'):
#    print(csv)
#    with open(csv) as csv_file:
#        x332s = pd.read_csv(csv, delimiter=';').drop(0)
#        if x332s.shape != (24, 9):
#            print(f'{csv} has an unexpected structure: {x332s.shape}')
#        #csv_reader = reader(csv_file, delimiter=';')
#        #csv_reader = DictReader(csv_file, delimiter=';')
#        #for row in csv_reader:
#        #    print(row)

with open('data/orc_2024.valid.json') as all_boats:
    x332s = [entry for entry in json.load(all_boats) if entry['boat']['type'] == 'X-332']

boat_speeds = defaultdict(list)

for entry in x332s:
    for angle in entry['vpp']['angles']:
        boat_speeds[angle].append(entry['vpp'][str(angle)])

avg_boat_speeds = { angle: np.mean(boat_speeds[angle], axis=0).tolist() for angle in boat_speeds}

with open('output/avg_x332.json', 'w') as avg_x332:
    json.dump(avg_boat_speeds, avg_x332, indent=4)
