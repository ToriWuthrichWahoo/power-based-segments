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
target = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]


fig, ax = plt.subplots(figsize=(5, 5))

ax.set_ylim([0, 11])
ax.set_xlim([0, 11])

(elevation_line,) = ax.plot([], [], color="red", lw=2)
(distance_line,) = ax.plot([], [], color="blue", lw=2)
(target_line,) = ax.plot(elevation, target, color="green", lw=2)


def animate_func(i):
    # ax.clear()
    # ax.set_xlim([0, 11])
    # ax.set_ylim([0, 11])
    # ax.scatter(distance[0:i], elevation[0:i])
    elevation_line.set_data(distance[0 : i + 1], elevation[0 : i + 1])
    distance_line.set_data(distance[0 : i + 1], distance[0 : i + 1])
    return elevation_line, distance_line


def init_fun():

    elevation_line.set_data([], [])
    distance_line.set_data([], [])
    return elevation_line, distance_line


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

plt.show()
