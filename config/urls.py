from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include([
        url('video/', include('rptp.video.urls.api')),
        url('auth/', include('rptp.users.urls.api'))
    ])),
    url('^', include([
        url('video/', include('rptp.video.urls.client', namespace='video')),
        url('auth/', include('rptp.users.urls.client')),
        url('', include('rptp.common.urls'))
    ], namespace='client')),
]
