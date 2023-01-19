import typing
import numpy as np
import pandas as pd


class Segment:
    def __init__(
        self,
        activity_df: pd.DataFrame(),
        segment_start_time_sec: int,
        segment_end_time_sec: int,
    ):
        """Initialize a segment object

        Parameters
        ----------
        activity_df : pd.Dataframe
            Dataframe from a records.csv file
        segment_start_time_sec : int
            Start time of the segment (sec)
        segment_end_time_sec : int
            End time of the segment (sec)
        """
        self.activity_df = activity_df
        self.segment_start_time_sec = segment_start_time_sec
        self.segment_end_time_sec = segment_end_time_sec
        self.segment_df = activity_df.loc[
            (activity_df.sec >= segment_start_time_sec)
            & (activity_df.sec <= segment_end_time_sec)
        ]
        self.true_finish_time = segment_end_time_sec - segment_start_time_sec

    def get_segment_avg_power(self) -> float:
        avg_watts = np.mean(self.segment_df["pwr_watts"])
        print(avg_watts)
        return avg_watts

    def get_int(self) -> int:
        return 1
