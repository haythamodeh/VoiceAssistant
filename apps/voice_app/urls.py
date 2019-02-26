from django.conf.urls import url
from.import views

urlpatterns = [
    url(r'^$', views.index),
    url(r"^myCommand$", views.myCommand),
    url(r"^voice$", views.voice),
    url(r"^clearActivityLog$", views.clearActivityLog),

    
]