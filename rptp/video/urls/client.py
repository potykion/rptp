from django.conf.urls import url

from rptp.video.views import video_search_template_view

urlpatterns = [
    url('search', video_search_template_view, name='search')
]
