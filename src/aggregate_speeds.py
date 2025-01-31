from collections import defaultdict
import json

import numpy as np

with open('../data/orc-data.json') as all_boats:
    x332s = [entry for entry in json.load(all_boats) if entry['boat']['type'] == 'X-332']

boat_speeds = defaultdict(list)

for entry in x332s:
    for angle in entry['vpp']['angles']:
        boat_speeds[angle].append(entry['vpp'][str(angle)])

    boat_speeds['beat_angle'].append(entry['vpp']['beat_angle'])
    boat_speeds['beating'].append((entry['vpp']['beat_vmg'] / np.cos(np.deg2rad(entry['vpp']['beat_angle']))).tolist())

    boat_speeds['run_angle'].append(entry['vpp']['run_angle'])
    boat_speeds['running'].append((entry['vpp']['run_vmg'] / np.cos(np.pi - np.deg2rad(entry['vpp']['run_angle']))).tolist())

avg_boat_speeds = { angle: np.round(np.mean(boat_speeds[angle], axis=0), 2).tolist() for angle in boat_speeds}
avg_boat_speeds['angles'] = entry['vpp']['angles']
avg_boat_speeds['speeds'] = entry['vpp']['speeds']
avg_boat_speeds['beat_angle'] = np.round(np.mean(boat_speeds['beat_angle'], axis=0), 1).tolist()
avg_boat_speeds['beating'] = np.round(np.mean(boat_speeds['beating'], axis=0), 2).tolist()
avg_boat_speeds['run_angle'] = np.round(np.mean(boat_speeds['run_angle'], axis=0), 1).tolist()
avg_boat_speeds['running'] = np.round(np.mean(boat_speeds['running'], axis=0), 2).tolist()

with open('../output/avg_x332.json', 'w') as avg_x332:
    json.dump(avg_boat_speeds, avg_x332, indent=4)
