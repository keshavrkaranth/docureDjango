from django.urls import path
from . import views

urlpatterns = [
  path('',views.homePage,name='homepage'),
  path('missions/',views.missions,name='missions'),
  path('about/',views.about,name='about'),
  path('gallery/',views.gallery_view,name='gallery'),
  path('category_product_description/<slug:catogery_slug>/<slug:product_slug>/',views.category_product_description,name='category_product_description')

]