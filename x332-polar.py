import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def interpolate_beat_and_run(boat_speeds):
    return pd.Series(boat_speeds).interpolate().tolist()

boat_speed = {
    6: [None, 4.6, 5.07, 5.34, 5.53, 5.42, 5.35, 5.16, 4.61, 4.13, 3.88, None],
    12: [6.1, None, 6.79, 6.98, 7.16, 7.2, 7.42, 7.36, 7.08, None, 6.62, 6.27],
}
wind_angle = [deg * np.pi / 180 for deg in [39.2, 43.6, 52, 60, 75, 90, 110, 120, 135, 144.4, 150, 158.3]]

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(wind_angle, interpolate_beat_and_run(boat_speed[6]))
ax.plot(wind_angle, interpolate_beat_and_run(boat_speed[12]))

ax.set_theta_direction(-1)  # clockwise
ax.set_theta_offset(np.pi / 2)  # rotate by 90 deg
ax.set_thetagrids((0, 45, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180))
ax.set_rmax(10)

print(interpolate_beat_and_run(boat_speed[6]))
print(interpolate_beat_and_run(boat_speed[12]))

plt.show()
