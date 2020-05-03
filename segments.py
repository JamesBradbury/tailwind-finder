from csv import DictReader, DictWriter
from typing import Dict

from stravalib import Client

from compassbearing import calculate_initial_compass_bearing


def get_bearing_for_segment(strava_client: Client, segment_id: int):
    segment_object = strava_client.get_segment(segment_id=segment_id)
    return calculate_initial_compass_bearing(
        point_a=tuple(segment_object.start_latlng),
        point_b=tuple(segment_object.end_latlng)
    )


def get_clean_segment_id(segment: Dict):
    """Returns segment ID as an int. Can handle ID as numeric string or as a segment URL string."""
    id = segment.get("ID")
    id_int = None
    if not id:
        raise AttributeError(f"No ID found for segment: {segment}")
    try:
        id_int = int(id)
    except ValueError:
        if id.startswith("http"):
            last_part_of_url = id.split("/")[-1:][0]
            try:
                id_int = int(last_part_of_url)
            except ValueError:
                raise ValueError(f"Invalid Segment URL {id}. Must end with an integer.")
    return id_int


