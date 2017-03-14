from django.conf.urls import url

from . import views

app_name = 'post'
urlpatterns = [
    url(r'^create/$', views.post_create, name='create'),
    url(r'^photo/add/$', views.post_photo_add, name='photo_add'),
    url(r'^list/$', views.post_list, name='list'),
]