from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="users_login"),
    url(r'^users/(?P<id>[0-9]*)', views.show, name="users_show")
]
