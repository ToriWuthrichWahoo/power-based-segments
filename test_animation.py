import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

import segment
from segment.segment import Segment
from segment_processor.segment_processor import SegmentProcessor

import imp

imp.reload(segment)

# Tori (App Gap)
df = pd.read_csv("data/2022-09-02-173454-ELEMNT BOLT 981E-274-0/test.records.csv")
segment_bounds_sec = (3468, 4742)
weight_kg = 57

# Robbie (App Gap)
# df = pd.read_csv('data/2022-09-02-173457-ELEMNT_BOLT_B471-1171-0/test.records.csv')
# segment_bounds_sec = (3428, 4653)
# weight_kg = 80

# s = Segment(df, segment_bounds_sec[0], segment_bounds_sec[1])

# p = SegmentProcessor(s, rider_weight_kg=weight_kg, equipment_weight_kg=12)
# (time_sec, dist_m, total_times, remaining_times) = p.power_based_finish_time()

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# s.segment_df.columns
# elevation  = s.segment_df["alt_m"].values

distance = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
elevation = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
est = [13, 14, 15, 16, 17, 13, 14, 15, 16, 17]
time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fig, ax = plt.subplots(figsize=(5, 5))
ax2 = ax.twinx()

ax.set_ylim([0, 11])
ax.set_xlim([0, 11])

ax2.set_ylim([10, 20])
ax2.set_xlim([0, 11])

(elevation_line,) = ax.plot(time, elevation, color="orange", lw=2)
(locator_dot,) = ax.plot(np.nan, np.nan, marker="o", color="blue")

(target_line,) = ax2.plot(elevation, target, color="green", lw=2)
(time_line,) = ax2.plot([], [], color="red", lw=2)


def animate_func(i):
    # ax.clear()
    # ax.set_xlim([0, 11])
    # ax.set_ylim([0, 11])
    # ax.scatter(distance[0:i], elevation[0:i])
    locator_dot.set_data(time[i], elevation[i])
    time_line.set_data(time[0 : i + 1], est[0 : i + 1])
    return locator_dot, time_line


def init_fun():

    locator_dot.set_data([], [])
    time_line.set_data(np.nan, np.nan)
    return locator_dot, time_line


# ax.plot(distance, elevation, label="Elevation Profile")
line_ani = animation.FuncAnimation(
    fig,
    animate_func,
    # interval=500,
    frames=len(distance),
    repeat=True,
    blit=True,
    init_func=init_fun,
)

# f = r"c://Users/toriwuthrich/Desktop/animate_func.gif"
# writergif = animation.PillowWriter(fps=len(distance)/6)
# line_ani.save(f, writer=writergif)

plt.legend()
plt.show()
