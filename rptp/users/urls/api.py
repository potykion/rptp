from django.conf.urls import url

from rptp.users.views import auth_api_view

urlpatterns = [
    url('^$', auth_api_view, name='auth')
]
