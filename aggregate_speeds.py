from collections import defaultdict
import json

import numpy as np

with open('data/orc_2024.valid.json') as all_boats:
    x332s = [entry for entry in json.load(all_boats) if entry['boat']['type'] == 'X-332']

boat_speeds = defaultdict(list)

for entry in x332s:
    for angle in entry['vpp']['angles']:
        boat_speeds[angle].append(entry['vpp'][str(angle)])

    boat_speeds['beat_angle'].append(entry['vpp']['beat_angle'])
    boat_speeds['beating'].append((entry['vpp']['beat_vmg'] / np.cos(np.deg2rad(entry['vpp']['beat_angle']))).tolist())

avg_boat_speeds = { angle: np.mean(boat_speeds[angle], axis=0).tolist() for angle in boat_speeds}
avg_boat_speeds['beat_angle'] = np.mean(boat_speeds['beat_angle'], axis=0).tolist()
avg_boat_speeds['beating'] = np.mean(boat_speeds['beating'], axis=0).tolist()
avg_boat_speeds['angles'] = entry['vpp']['angles']
avg_boat_speeds['speeds'] = entry['vpp']['speeds']

with open('output/avg_x332.json', 'w') as avg_x332:
    json.dump(avg_boat_speeds, avg_x332, indent=4)
