from django.conf.urls import url

from rptp.common.views import main_view

urlpatterns = [
    url('^$', main_view, name='main')
]
