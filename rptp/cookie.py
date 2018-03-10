def save_token_data(response, access_token, user_id=None):
    response.cookies['access_token'] = access_token

    if user_id:
        response.cookies['user_id'] = str(user_id)
    return response


def get_token(request):
    return request.cookies.get('access_token')
