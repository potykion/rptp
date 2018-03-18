DAY_SECONDS = 3600 * 24


def save_token_data(response, access_token, user_id=None):
    response.cookies['access_token'] = access_token
    response.cookies['access_token']['max-age'] = DAY_SECONDS

    if user_id:
        response.cookies['user_id'] = str(user_id)
    return response
