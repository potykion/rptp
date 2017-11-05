from unittest import mock

import pytest
from django.test import Client
from django.urls import reverse

from rptp.users.models import User


@pytest.fixture()
def code():
    return '925b8aa9acac4133ba'


@pytest.fixture()
def auth_link():
    return 'https://oauth.vk.com/authorize?client_id=6030754&redirect_uri=https%3A%2F%2Frptp.herokuapp.com%2Fauth&scope=video%2C+offline&v=5.68&response_type=code&display=mobile'


@pytest.fixture()
def auth_token():
    return '19e2cdb1ee6e085588f1c1e0937cd31881285e06b325c82581f0c9351a11eee22fe128d6916f5b5b81823'


@pytest.fixture()
def token_data():
    return {
        'access_token': '19e2cdb1ee6e085588f1c1e0937cd31881285e06b325c82581f0c9351a11eee22fe128d6916f5b5b81823',
        'expires_in': 0,
        'user_id': 16231309
    }


@pytest.fixture()
def invalid_code_data():
    return {
        'error': 'invalid_grant',
        'error_description': 'Code is invalid or expired.'
    }


@pytest.mark.django_db
def test_auth_view_with_code(client: Client, code, token_data):
    """
    Given client,
    When go to auth view with code argument,
    Then response contains user_id and token,
    And user with response created.
    """
    with mock.patch('rptp.vk.utils.auth.receive_token_from_code') as receiced_token:
        receiced_token.return_value = token_data
        response = client.get('{}?code={}'.format(reverse('auth'), code))

    assert response.data == {
        'user_id': token_data['user_id'],
        'access_token': token_data['access_token']
    }

    user = User.objects.filter(user_id=token_data['user_id']).get()
    assert user.access_token == token_data['access_token']


def test_auth_view_without_code(client: Client, auth_link):
    """
    Given client,
    When go to auth view without code-argument,
    Then response contains auth url.
    """

    with mock.patch('rptp.vk.utils.auth.generate_auth_link') as generate_link_mock:
        generate_link_mock.return_value = auth_link
        response = client.get(reverse('auth'))

    assert response.data == {
        "auth_url": auth_link
    }


def test_auth_view_with_invalid_code(client: Client, code, invalid_code_data, auth_link):
    """
    Given client, code,
    When go to auth view with invalid code,
    Then response contains auth url.
    """

    with mock.patch('rptp.vk.utils.auth.receive_token_from_code') as invalid_code_mock:
        invalid_code_mock.return_value = invalid_code_data

        with mock.patch('rptp.vk.utils.auth.generate_auth_link') as generate_link_mock:
            generate_link_mock.return_value = auth_link

            response = client.get(reverse('auth'))

    assert response.data == {
        "auth_url": auth_link
    }


@pytest.mark.django_db
def test_auth_template_view(client: Client, code, token_data):
    """
    Given client, code,
    When go to auth_template_view with code,
    Then user is created and logged in.
    """
    with mock.patch('requests.get') as vk_response:
        vk_response.return_value = mock.MagicMock(
            json=lambda: token_data,
        )
        client.get('{}?{}'.format(
            reverse('client:auth'),
            'code={}'.format(code)
        ))

    assert User.objects.get(user_id=token_data['user_id'])




