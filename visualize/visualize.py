import numpy as np
import matplotlib.pyplot as plt


class Animator:
    def __init__(
        self,
        save: bool,
        save_path: str,
        distance_m: np.array,
        elevation_m: np.array,
        time_est: np.array,
        time_actual: float,
    ):
        self.save = save
        self.save_path = save_path
        self.distance_m = distance_m
        self.elevation_m = elevation_m
        self.time_est = time_est
        self.time_actual = time_actual
    
        def animate_func(i):
            locator_dot.set_data(time[i], elevation[i])
            time_line.set_data(time[0 : i + 1], est[0 : i + 1])
            return locator_dot, time_line

    def run(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax2 = ax.twinx()

        ax.set_ylim([np.min(self.elevation_m) - 5, np.max(self.elevation_m) + 5])
        ax.set_xlim([np.min(self.distance_m), np.max(self.distance_m)])
        ax2.set_ylim([np.min(self.time_est) - 5, np.max(self.time_est) + 5])

        (elevation_line,) = ax.plot(
            self.distance_m,
            self.elevation_m,
            color="orange",
            lw=2,
            label="Elevation Profile",
        )
        (locator_dot,) = ax.plot(
            np.nan, np.nan, marker="o", color="blue", label="Current Location"
        )

        (target_line,) = ax2.plot(
            self.distance_m,
            self.time_actual * np.ones(len(self.distance_m)),
            color="green",
            linestyle="dashed",
            lw=2,
            label="Target Time",
        )
        (time_line,) = ax2.plot([], [], color="red", lw=2)
        
       


def init_fun():

    locator_dot.set_data([], [])
    time_line.set_data(np.nan, np.nan)
    return locator_dot, time_line

        plt.show()
