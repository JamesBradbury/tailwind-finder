from stravalib import Client

import local_settings


def get_strava_client(verbose=False):

    strava_client: Client = Client()
    authorize_url = strava_client.authorization_url(client_id=local_settings.STRAVA_CLIENT_ID,
                                                    redirect_uri='http://localhost:8282/authorized')
    if verbose:
        print("authorize_url:", authorize_url)
    # NOTE: Need to start by pasting this into the browser and Authorizing it.
    # Instructions here: https://developers.strava.com/docs/getting-started/#oauth
    # http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read
    # Copy-paste code from resulting URL param "code="
    #
    # token_response = strava_client.exchange_code_for_token(client_id=local_settings.STRAVA_CLIENT_ID,
    #                                                        client_secret=local_settings.STRAVA_CLIENT_SECRET,
    #                                                        code=code)
    # print(token_response)
    # exit()

    # Once the token response has been received, it will work for a while, so can be stored locally.
    access_token = local_settings.TOKEN_RESPONSE['access_token']
    refresh_token = local_settings.TOKEN_RESPONSE['refresh_token']
    expires_at = local_settings.TOKEN_RESPONSE['expires_at']

    # Now store that short-lived access token somewhere (a database?)
    strava_client.access_token = access_token
    # You must also store the refresh token to be used later on to obtain another valid access token
    # in case the current is already expired
    strava_client.refresh_token = refresh_token

    # An access_token is only valid for 6 hours, store expires_at somewhere and
    # check it before making an API call.
    strava_client.token_expires_at = expires_at
    if verbose:
        athlete = strava_client.get_athlete()
        print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))

    # Use refresh tokens here:
    # https://developers.strava.com/docs/authentication/#refreshingexpiredaccesstokens

    return strava_client
