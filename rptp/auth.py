from sanic.response import html

from rptp import vk_api
from rptp.cookie import save_token_data


class VKResponseAuthorizer:
    async def authorize_response(self, response, code):
        token_data = await vk_api.request_token_data(code)
        user_id, access_token = token_data['user_id'], token_data['access_token']
        response = save_token_data(response, access_token, user_id)
        return response

    async def create_authorization_response(self, template):
        auth_link = vk_api.generate_auth_link()
        context = {'auth_link': auth_link}

        rendered = await template.render_async(**context)
        return html(rendered)


def extract_auth_data(request):
    return request.headers.get('authorization') or \
           request.args.get('token') or \
           request.cookies.get('access_token')
