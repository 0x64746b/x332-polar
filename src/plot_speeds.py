import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from great_tables import GT


def interpolate_beat_and_run(sparse_speeds: pd.DataFrame):
    return sparse_speeds.interpolate(method='index', axis=1, limit_area='inside').round(1)

# Read data
with open('../output/avg_x332.json') as avg_speeds:
    data = json.load(avg_speeds)

# Prepare data structures
wind_angles = np.unique(np.rint(data['beat_angle'] + data['angles'] + data['run_angle']).astype(int))
boat_speeds = pd.DataFrame(index=data['speeds'], columns=wind_angles, dtype=np.float64)

# Construct data frame from raw values
for angle in data['angles']:
    boat_speeds[angle] = np.round(data[str(angle)], 1)

for tws, twa, boat_speed in zip(data['speeds'], np.rint(data['beat_angle']), np.round(data['beating'], 1)):
    boat_speeds.at[tws, twa] = boat_speed

for tws, twa, boat_speed in zip(data['speeds'], np.rint(data['run_angle']), np.round(data['running'], 1)):
    boat_speeds.at[tws, twa] = boat_speed

pd.options.display.width=None
print(boat_speeds)

(
    GT(boat_speeds.assign(TWS=data['speeds']), rowname_col='TWS')
    .tab_header(title="X-332", subtitle='Avg. target speeds')
    #.tab_stubhead(label="TWS\TWA")
    .opt_stylize(style=1)
    .opt_horizontal_padding(scale=2)
).show()

# Plot the whole thing
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig.canvas.manager.set_window_title('X-332 Polar Diagram')

interpolate_beat_and_run(boat_speeds).apply(lambda speed_at_angle: ax.plot(np.deg2rad(wind_angles), speed_at_angle), axis=1)

ax.set_theta_direction(-1)  # clockwise
ax.set_theta_offset(np.pi / 2)  # rotate by 90 deg
ax.set_thetamin(0)  # plot only right half of diagram
ax.set_thetamax(180)
ax.set_thetagrids((0, 45, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180))
ax.set_rmax(10)
ax.grid(linestyle=':')

plt.show()
