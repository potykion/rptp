from django.conf.urls import url

from rptp.users.views import auth_user_view

urlpatterns = [
    url('^$', auth_user_view, name='auth')
]