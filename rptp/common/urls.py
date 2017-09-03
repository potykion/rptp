from django.conf.urls import url
from django.conf.urls.static import static

from config.settings import common
from rptp.common.views import index_view

urlpatterns = [
                  url(r'^$', index_view)
              ]