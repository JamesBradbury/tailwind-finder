from csv import DictWriter
from typing import Dict, Set

from stravalib.model import Segment

from get_strava_client import get_strava_client
from compassbearing import calculate_initial_compass_bearing
from local_settings import DEFAULT_MINIMUM_SCORE


class UserSegment:
    """
    Segment with additional derived/user data.
    """
    bearing = 0
    threshold_score_to_report = DEFAULT_MINIMUM_SCORE

    def __init__(self, segment: Dict):
        self.strava_id = segment["strava_id"]
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


class SegmentsArchive:
    """Class to download segment data and store it locally."""
    segments_list = []
    strava_client = None

    def __init__(self, new_client):
        self.strava_client = new_client

    def read_segments(self, segments_ids: Set):
        for seg_id in segments_ids:
            new_segment = self.strava_client.get_segment(segment_id=seg_id)
            self.segments_list.append(UserSegment.from_stravalib_segment_object(segment_obj=new_segment))

    def write_segments_to_csv(self):
        """Writes the segments_dict to a local CSV file for temporary storage."""
        header = ["strava_id", "name", "start_latlng", "end_latlng", "bearing", "threshold_score_to_report"]
        with open("full_segment_data.csv", "w") as full_segment_csv_file:
            csv_writer = DictWriter(full_segment_csv_file, fieldnames=header)
            csv_writer.writeheader()
            for segment in self.segments_list:
                csv_writer.writerow(
                    rowdict=dict(
                        strava_id=segment.strava_id,
                        name=segment.name_str,
                        start_latlng=segment.start_latlng,
                        end_latlng=segment.end_latlng,
                        bearing=segment.bearing,
                        threshold_score_to_report=segment.threshold_score_to_report
                    )
                )


# Exploratory code to write segment data locally (less spamming Strava client)
# new_strava_client = get_strava_client(verbose=True)
# new_segments_archive = SegmentsArchive(new_strava_client)
# starred_segs = new_strava_client.get_starred_segments()
# seg_ids = {seg.id for seg in starred_segs}  # if seg.activity_type == "Ride"}
# 
# new_segments_archive.read_segments(segments_ids=seg_ids)
# 
# athlete_segments = [(s.strava_id, s.name_str) for s in new_segments_archive.segments_list]
# for sid, name_str in athlete_segments:
#     print(f"Segment: {sid} {name_str}")
# new_segments_archive.write_segments_to_csv()
