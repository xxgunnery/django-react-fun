from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name='index'),
  path("change", views.change),
  path("getGameSessionData", views.getGameSessionData),
  path("getUserData", views.getUserData),
  path("getDoLLStats", views.getDoLLStats),
]