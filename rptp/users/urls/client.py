from django.conf.urls import url

from rptp.users.views import auth_template_view

urlpatterns = [
    url('^$', auth_template_view, name='auth')
]
