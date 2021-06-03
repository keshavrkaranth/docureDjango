from django.urls import path
from . import views

urlpatterns = [
  path('',views.homePage,name='homepage'),
  path('missions/',views.missions,name='missions'),
  path('about/',views.about,name='about'),

]