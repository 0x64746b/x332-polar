from collections import defaultdict
import json
from typing import List

import numpy as np


def filter_by_type(all_boats: List, boat_type: str) -> List:
    return [entry for entry in all_boats if entry['boat']['type'] == boat_type]


def average_data(boats: List):
    boat_speeds = defaultdict(list)

    for entry in boats:
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

    return avg_boat_speeds


def main(data_filename: str, boat_type: str, output_filename: str):
    with open(data_filename) as all_boats:
        relevant_boats = filter_by_type(json.load(all_boats), boat_type)

    avg_boat_speeds = average_data(relevant_boats)

    with open(output_filename, 'w') as output_file:
        json.dump(avg_boat_speeds, output_file, indent=4)


if __name__ == '__main__':
    main('../data/orc-data.json', 'X-332', '../output/X-332_Averaged_Speeds.json')
