from django.conf.urls import url
from rest_framework.authtoken import views as auth_token_views

from .. import apis

urlpatterns = [
    url(r'^token-auth/', auth_token_views.obtain_auth_token),
    url(r'^profile/', apis.ProfileView.as_view()),

    url(r'^token-delete/$', apis.DeleteToken.as_view()),
]
