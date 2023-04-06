from django.urls import re_path
from hearts import views

urlpatterns = [
    re_path(r'^api/hearts$', views.heart_list),
    re_path(r'^api/hearts/(?P<pk>[0-9]+)$', views.heart_detail),
    # re_path(r'^api/v1/hearts$', views.heart_list_v1)
]
