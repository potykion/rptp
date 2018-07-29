from jinja2 import Template
from sanic.response import html, HTTPResponse

from rptp import vk_api
from rptp.cookie import save_token_data


async def create_authorized_template_response(template: Template, code: str) -> HTTPResponse:
    rendered_html = await template.render_async()
    response_ = html(rendered_html)

    if code:
        authorized_response = await authorize_response(response_, code)
    else:
        authorized_response = response_

    return authorized_response


async def authorize_response(response, code):
    token_data = await vk_api.request_token_data(code)
    user_id, access_token = token_data['user_id'], token_data['access_token']
    response = save_token_data(response, access_token, user_id)
    return response


async def create_authorization_template_response(template: Template) -> HTTPResponse:
    auth_link = vk_api.generate_auth_link()
    context = {'auth_link': auth_link}

    rendered = await template.render_async(**context)
    return html(rendered)


def extract_auth_data(request):
    return request.headers.get('authorization') or \
           request.args.get('token') or \
           request.cookies.get('access_token')
