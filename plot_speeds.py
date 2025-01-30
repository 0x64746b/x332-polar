import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def interpolate_beat_and_run(boat_speeds):
    stripped_speeds = list(boat_speeds)
    trailing_nans = []

    while stripped_speeds[-1] is np.nan:
        trailing_nans.append(stripped_speeds.pop())

    return pd.Series(stripped_speeds).interpolate().tolist() + trailing_nans

# Read data
with open('output/avg_x332.json') as avg_speeds:
    data = json.load(avg_speeds)

# Prepare data structures
wind_angles = sorted(data['beat_angle'] + data['angles'] + data['run_angle'])
boat_speeds = pd.DataFrame(index=data['speeds'], columns=wind_angles)

# Construct data frame from raw values
for angle in data['angles']:
    boat_speeds[angle] = data[str(angle)]

for tws, twa, boat_speed in zip(data['speeds'], data['beat_angle'], data['beating']):
    boat_speeds.at[tws, twa] = boat_speed

for tws, twa, boat_speed in zip(data['speeds'], data['run_angle'], data['running']):
    boat_speeds.at[tws, twa] = boat_speed

# Plot the whole thing
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig.canvas.manager.set_window_title('X-332 Polar Diagram')

boat_speeds.apply(lambda speed_at_angle: ax.plot(np.deg2rad(wind_angles), interpolate_beat_and_run(speed_at_angle)), axis=1)

ax.set_theta_direction(-1)  # clockwise
ax.set_theta_offset(np.pi / 2)  # rotate by 90 deg
ax.set_thetamin(0)  # plot only right half of diagram
ax.set_thetamax(180)
ax.set_thetagrids((0, 45, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180))
ax.set_rmax(10)
ax.grid(linestyle=':')

plt.show()
