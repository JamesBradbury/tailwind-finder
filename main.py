from get_strava_client import get_strava_client

from stravalib.attributes import LatLon


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

# segment_bearing = get_bearing_for_segment(strava_client=strava_client, segment_id=6665302)
# print("segment_bearing:", segment_bearing)  # 93.140334170389

segments_with_headings = []
# with open("local_segments.csv", mode="r") as local_csv:
#     csv_reader = DictReader(local_csv)
#     for segment in csv_reader:
#         updated_segment = segment.copy()
#         segment_id = get_clean_segment_id(segment=segment)
#         # updated_segment["bearing"] = # get_bearing_for_segment(strava_client=strava_client, segment_id=segment_id)
#         segments_with_headings.append(updated_segment)
#
# for seg in segments_with_headings:
#     print(seg["Name"], seg["ID"], seg["bearing"])

