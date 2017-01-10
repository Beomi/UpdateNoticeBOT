from django.conf.urls import url
from .views import custom_notice


urlpatterns = [
    url(r'^custom_notice/$', custom_notice, name='custom_notice'),
]