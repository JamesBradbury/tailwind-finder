import local_settings
from stravalib.client import Client

strava_client = Client()
authorize_url = strava_client.authorization_url(client_id=local_settings.STRAVA_CLIENT_ID,
                                                redirect_uri='http://localhost:8282/authorized')
print("authorize_url:", authorize_url)
# NOTE: Need to start by pasting this into the browser and Authorizing it.
# Instructions here: https://developers.strava.com/docs/getting-started/#oauth
# http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code
# &redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read
# Copy-paste code from resulting URL param "code="
code = "b65175375ca081f48c0beae3dfe320e4283ef58e"

token_response = strava_client.exchange_code_for_token(client_id=local_settings.STRAVA_CLIENT_ID,
                                                       client_secret=local_settings.STRAVA_CLIENT_SECRET,
                                                       code=code)
access_token = token_response['access_token']
refresh_token = token_response['refresh_token']
expires_at = token_response['expires_at']

# Now store that short-lived access token somewhere (a database?)
strava_client.access_token = access_token
# You must also store the refresh token to be used later on to obtain another valid access token
# in case the current is already expired
strava_client.refresh_token = refresh_token

# An access_token is only valid for 6 hours, store expires_at somewhere and
# check it before making an API call.
strava_client.token_expires_at = expires_at

athlete = strava_client.get_athlete()
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))
print(athlete)
cheddar_gorge_segment_id = 6665302
cheddar_gorge = strava_client.get_segment(segment_id=cheddar_gorge_segment_id)
print(dir(cheddar_gorge))
print(cheddar_gorge.start_latlng, cheddar_gorge.end_latlng)
# Sanity-check the output of start_latlng:
# https://www.latlong.net/c/?lat=51.27987&long=-2.77271


