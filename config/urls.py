from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include([
        url('video', include('rptp.video.urls')),
        url('auth', include('rptp.users.urls'))
    ]))
]
