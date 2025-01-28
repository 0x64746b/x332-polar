from collections import defaultdict
import json

import numpy as np

with open('data/orc_2024.valid.json') as all_boats:
    x332s = [entry for entry in json.load(all_boats) if entry['boat']['type'] == 'X-332']

boat_speeds = defaultdict(list)

for entry in x332s:
    for angle in entry['vpp']['angles']:
        boat_speeds[angle].append(entry['vpp'][str(angle)])

avg_boat_speeds = { angle: np.mean(boat_speeds[angle], axis=0).tolist() for angle in boat_speeds}

with open('output/avg_x332.json', 'w') as avg_x332:
    json.dump(avg_boat_speeds, avg_x332, indent=4)
