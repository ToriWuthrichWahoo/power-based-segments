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
        power_scale_factor=0.96,
    ):
        self.segment = segment
        self.m_total = rider_weight_kg + equipment_weight_kg
        self.c_RR = c_RR
        self.cda = cda
        self.epsilon = 1e-2
        self.power_scale_factor = power_scale_factor

    def estimate_finish_time(self):
        # Test method to calculate speed as a function of time
        time_s = self.segment.segment_df["sec"].values
        t0_s = time_s[0]
        s0_mps = self.segment.segment_df["spd_mps"].values[0]
        grade = 0.01 * self.segment.segment_df["grade_perc"].values
        power = self.power_scale_factor * self.segment.segment_df["pwr_watts"].values
        spd_out = np.zeros(len(time_s))

        # Initialize to current speed
        spd_out[0] = s0_mps
        for i in range(1, len(time_s)):

            s = spd_out[i - 1]
            power_i = power[i]
            grade_i = grade[i]
            dt = time_s[i] - time_s[i - 1]

            f_wind = 0.5 * self.cda * s**2
            f_rolling = self.m_total * 9.806 * self.c_RR
            f_slope = self.m_total * 9.806 * grade_i
            if s > self.epsilon:
                f_rider = power_i / s
            else:
                f_rider = 0

            a = (f_rider - f_wind - f_rolling - f_slope) / self.m_total
            spd_out[i] = s + a * dt

        return spd_out
