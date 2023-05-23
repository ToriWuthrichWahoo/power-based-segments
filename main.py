import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D

import segment
from segment.segment import Segment
from segment_processor.segment_processor import SegmentProcessor

import imp

imp.reload(segment)

# Tori (Washington)
# df = pd.read_csv("data/2022-08-20-123002-ELEMNT_BOLT_981E-266-0/test.records.csv")
# segment_bounds_sec = (34, 5362)
# weight_kg = 57

# Tori (App Gap)
df = pd.read_csv("data/2022-09-02-173454-ELEMNT BOLT 981E-274-0/test.records.csv")
segment_bounds_sec = (3468, 4742)
weight_kg = 77  # artifically increase by 20 kg

# Robbie (App Gap)
# df = pd.read_csv("data/2022-09-02-173457-ELEMNT_BOLT_B471-1171-0/test.records.csv")
# segment_bounds_sec = (3428, 4653)
# weight_kg = 80

s = Segment(df, segment_bounds_sec[0], segment_bounds_sec[1])

p = SegmentProcessor(s, rider_weight_kg=weight_kg, equipment_weight_kg=12)
(time_sec, dist_m, total_times, remaining_times) = p.power_based_finish_time()

elevation_m = s.segment_df["alt_m"].values
actual_time = s.segment_df["sec"].values[-1] - s.segment_df["sec"].values[0]

#### POST PROCESS ####
total_times_filtered = np.zeros(len(total_times))
for j in range(len(total_times)):
    total_times_filtered[j] = np.mean(total_times[max(0, j - 10) : j + 1])

#### VISUALIZE ####
dist_m = dist_m - dist_m[0]
fig, ax = plt.subplots(figsize=(5, 5))
ax2 = ax.twinx()

ax.set_xlabel("Distance (m)")
ax.set_ylim([np.min(elevation_m) - 5, np.max(elevation_m) + 5])
ax.set_ylabel("Elevation (m)")
ax.set_xlim([np.min(dist_m), np.max(dist_m)])
ax2.set_ylim([np.min(total_times_filtered) - 5, np.max(total_times_filtered) + 5])
ax2.set_ylabel("Time (s)")

(elevation_line,) = ax.plot(
    dist_m,
    elevation_m,
    color="orange",
    lw=2,
)
(locator_dot,) = ax.plot(np.nan, np.nan, marker="o", color="blue")

(target_line,) = ax2.plot(
    dist_m,
    actual_time * np.ones(len(dist_m)),
    color="green",
    linestyle="dashed",
    lw=2,
)
(time_line,) = ax2.plot([], [], color="red", lw=2)


def animate_func(i):
    locator_dot.set_data(dist_m[i], elevation_m[i])
    time_line.set_data(dist_m[0 : i + 1], total_times_filtered[0 : i + 1])
    return locator_dot, time_line


def init_fun():
    locator_dot.set_data([], [])
    time_line.set_data(np.nan, np.nan)
    return locator_dot, time_line


line_ani = animation.FuncAnimation(
    fig,
    animate_func,
    frames=len(dist_m),
    interval=10,
    repeat=True,
    blit=True,
    init_func=init_fun,
)


line1 = Line2D([0], [0], color="orange", label="Elevation Profile")
line2 = Line2D(
    [0],
    [0],
    color="green",
    linestyle="dashed",
    label="Actual Finish Time (s)",
)
line3 = Line2D([0], [0], color="red", label="Estimated Finish Time (s)")

handles = [line1, line2, line3]
plt.legend(handles=handles)
plt.title("Finish Time Estimation")


plt.show()

# Saving the Animation
f = r"/Users/toriwuthrich/Desktop/animate_func.gif"
writergif = animation.PillowWriter(fps=len(dist_m) / 12)
line_ani.save(f, writer=writergif)
