def save_token_data(response, user_id, token):
    response.cookies['access_token'] = token
    response.cookies['user_id'] = str(user_id)
    return response
