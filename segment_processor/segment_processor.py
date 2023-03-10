import numpy as np
import pandas as pd
from segment.segment import Segment


class SegmentProcessor:
    def __init__(
        self,
        segment: Segment,
        rider_weight_kg=57,
        equipment_weight_kg=10,
        c_RR=0.005,
        cda=0.5,
        drive_train_efficiency=0.9,
    ):
        self.segment = segment
        self.m_total = rider_weight_kg + equipment_weight_kg
        self.c_RR = c_RR
        self.cda = cda
        self.epsilon = 1e-2
        self.drive_train_efficiency = drive_train_efficiency

    def power_based_finish_time(self):
        s0_mps = self.segment.segment_df["spd_mps"].values
        x0_m = self.segment.segment_df["dist_m"].values
        t = self.segment.segment_df["sec"].values
        remaining_times = np.zeros(len(x0_m))
        total_times = np.zeros(len(x0_m))

        # Each time we want to update the prediction, we know where we currently are, and how fast we are going based on the GPS.
        for i in range(len(x0_m)):
            (
                predicted_time,
                predicted_dist,
                predicted_spd,
            ) = self.estimate_time_to_finish(x0_m[i], s0_mps[i])

            remaining_times[i] = predicted_time[-1]
            total_times[i] = (t[i] - t[0]) + predicted_time[-1]
        return (t, x0_m, total_times, remaining_times)

    def estimate_time_to_finish(
        self,
        segment_distance_traveled_m: float,
        initial_speed_mps: float,
        power_window_sec=60,
    ):
        # Test method to calculate speed as a function of time

        grade = 0.01 * self.segment.segment_df["grade_perc"].values
        dist = self.segment.segment_df["dist_m"].values
        spd_out = [initial_speed_mps]
        x_out = [segment_distance_traveled_m]

        # Initialize to current speed
        t_out = [0]
        dt = 1
        i = 1

        while True:
            t_out.append(t_out[i - 1] + dt)
            s = spd_out[i - 1]
            x = x_out[i - 1]

            power_i = self.get_avg_power_last_n_sec(t_out[i], power_window_sec)

            # Get the grade based on where we are in the elevation profile
            grade_id = np.argmin(abs(dist - x_out[i - 1]))
            grade_i = grade[grade_id]

            f_wind = 0.5 * self.cda * (s**2)
            f_rolling = self.m_total * 9.806 * self.c_RR
            f_slope = self.m_total * 9.806 * grade_i
            if s > self.epsilon:
                f_rider = self.drive_train_efficiency * power_i / s
            else:
                f_rider = 0

            a = (f_rider - f_wind - f_rolling - f_slope) / self.m_total
            spd_out.append(s + a * dt)
            x_out.append(x + s * dt)

            # If we've crossed the end distance, break out of the loop
            if x_out[i] >= dist[-1]:
                break
            i += 1

        return t_out, x_out, spd_out

    def get_avg_power_last_n_sec(self, t, window_size_sec):
        power = self.segment.segment_df["pwr_watts"].values
        start_id = max(1, t - window_size_sec)
        power_window = power[start_id:t]
        if len(power_window) > 0:
            return np.mean(power[start_id:t])
        else:
            return power[start_id]
