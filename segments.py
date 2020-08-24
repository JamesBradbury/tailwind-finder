from typing import Dict

from stravalib.model import Segment

from compassbearing import calculate_initial_compass_bearing
from local_settings import DEFAULT_MINIMUM_SCORE


class UserSegment:
    """
    Segment with additional derived/user data.
    """
    bearing = 0
    threshold_score_to_report = DEFAULT_MINIMUM_SCORE

    def __init__(self, segment: Dict):
        self.strava_id = self.get_clean_segment_id(segment=segment)
        self.name_str = segment["name"]
        self.start_latlng = segment["start_latlng"]
        self.end_latlng = segment["end_latlng"]
        self.bearing = calculate_initial_compass_bearing(
            point_a=tuple(self.start_latlng),
            point_b=tuple(self.end_latlng)
        )

    @classmethod
    def from_stravalib_segment_object(cls, segment_obj: Segment):
        new_segment = dict(
            strava_id=segment_obj.id,
            name=segment_obj.name,
            start_latlng=segment_obj.start_latlng,
            end_latlng=segment_obj.end_latlng
        )
        return cls(new_segment)

    def header_for_csv(self):
        return "strava_id,name,start_latlng,end_latlng,threshold_score_to_report"

    def row_for_csv(self):
        return ",".join([

        ])

    @staticmethod
    def get_clean_segment_id(segment: Dict) -> int:
        """Returns segment ID as an int. Can handle ID as numeric string or as a segment URL string."""
        segment_id = segment.get("id")
        if not segment_id:
            raise AttributeError(f"No ID found for segment: {segment}")
        id_int = None
        try:
            id_int = int(segment_id)
        except ValueError:
            if segment_id.startswith("http"):
                last_part_of_url = segment_id.split("/")[-1:][0]
                try:
                    id_int = int(last_part_of_url)
                except ValueError:
                    raise ValueError(f"Invalid Segment URL {segment_id}. Must end with an integer.")
        return id_int
