from rptp import vk_api


class VKAuthorizer:
    async def auth(self, code):
        token_data = await vk_api.request_token_data(code)
        return token_data['user_id'], token_data['access_token']

    def generate_auth_link(self):
        return vk_api.generate_auth_link()
