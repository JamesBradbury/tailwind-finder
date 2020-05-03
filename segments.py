from csv import DictReader, DictWriter
from typing import Dict

from stravalib.attributes import LatLon

from compassbearing import calculate_initial_compass_bearing
from get_strava_client import get_strava_client


def get_bearing_for_segment(segment_id: int):
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
                raise AttributeError(f"Invalid Segment URL {id}. Must end with an integer.")
    return id_int


strava_client = get_strava_client(verbose=True)

# Cheddar Gorge example
cheddar_gorge_segment_id = 6665302
cheddar_gorge = strava_client.get_segment(segment_id=cheddar_gorge_segment_id)
print(dir(cheddar_gorge))
print("Start LatLong:", cheddar_gorge.start_latlng)
print("End LatLong:", cheddar_gorge.end_latlng)
# Sanity-check the output of start_latlng:
# https://www.latlong.net/c/?lat=51.27987&long=-2.77271

start_latlong = tuple(LatLon(lat=51.27987, lon=-2.77271))
end_latlong = tuple(LatLon(lat=51.278704, lon=-2.738877))

segment_bearing = get_bearing_for_segment(segment_id=6665302)
print("segment_bearing:", segment_bearing)  # 93.140334170389

segments_with_headings = []
with open("local_segments.csv", mode="r") as local_csv:
    csv_reader = DictReader(local_csv)
    for segment in csv_reader:
        updated_segment = segment.copy()
        segment_id = get_clean_segment_id(segment=segment)
        updated_segment["Bearing"] = get_bearing_for_segment(segment_id=segment_id)
        segments_with_headings.append(updated_segment)

for seg in segments_with_headings:
    print(seg["Name"], seg["ID"], seg["Bearing"])

