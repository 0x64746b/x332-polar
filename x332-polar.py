import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def interpolate_beat_and_run(boat_speeds):
    stripped_speeds = list(boat_speeds)
    trailing_nones = []

    while stripped_speeds[-1] is None:
        trailing_nones.append(stripped_speeds.pop())

    return pd.Series(stripped_speeds).interpolate().tolist() + trailing_nones

# https://jieter.github.io/orc-data/site/index.html#ITA/ITA13672
wind_angles = [38.9, 39, 39.2, 39.3, 39.9, 40.6, 41.1, 43.6, 52, 60, 75, 90, 110, 120, 135, 144.4, 149.4, 150, 152.8, 158.3, 170.9, 178.1, 178.8, 179]
boat_speeds = {
     #  [38.9, 39.0, 39.2, 39.3, 39.9, 40.6, 41.1, 43.6,   52,   60,   75,   90,  110,  120,  135, 144.4, 149.4, 150, 152.8, 158.3, 170.9, 178.1, 178.8, 179]
     6: [None, None, None, None, None, None, None, 4.60, 5.07, 5.34, 5.53, 5.42, 5.35, 5.16, 4.61, 4.13, None, 3.88, None, None, None, None, None, None],
     8: [None, None, None, None, None, None, 5.35, None, 5.97, 6.21, 6.39, 6.34, 6.43, 6.27, 5.72, None, 5.01, 4.97, None, None, None, None, None, None],
    10: [None, None, None, None, 5.87, None, None, None, 6.53, 6.72, 6.87, 6.91, 7.03, 6.95, 6.56, None, None, 5.90, 5.76, None, None, None, None, None],
    12: [None, None, 6.10, None, None, None, None, None, 6.79, 6.98, 7.16, 7.20, 7.42, 7.36, 7.08, None, None, 6.62, None, 6.27, None, None, None, None],
    14: [None, 6.22, None, None, None, None, None, None, 6.89, 7.10, 7.36, 7.45, 7.75, 7.73, 7.48, None, None, 7.10, None, None, 6.52, None, None, None],
    16: [6.26, None, None, None, None, None, None, None, 6.94, 7.16, 7.48, 7.68, 8.01, 8.08, 7.87, None, None, 7.47, None, None, None, 6.94, None, None],
    20: [None, None, None, 6.31, None, None, None, None, 7.00, 7.23, 7.62, 7.99, 8.33, 8.68, 8.65, None, None, 8.22, None, None, None, None, None, 7.66],
    24: [None, None, None, None, None, 6.28, None, None, 6.97, 7.22, 7.69, 8.16, 8.47, 9.06, 9.65, None, None, 9.08, None, None, None, None, 8.38, None],
}

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

for _, speed_at_angle in sorted(boat_speeds.items()):
    ax.plot(np.deg2rad(wind_angles), interpolate_beat_and_run(speed_at_angle))

ax.set_theta_direction(-1)  # clockwise
ax.set_theta_offset(np.pi / 2)  # rotate by 90 deg
ax.set_thetamin(0)  # plot only right half of diagram
ax.set_thetamax(180)
ax.set_thetagrids((0, 45, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180))
ax.set_rmax(10)

plt.show()
