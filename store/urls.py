from django.urls import path
from . import views

urlpatterns = [
    path('',views.products,name='products'),
    path('<slug:category_slug>/',views.products,name='products_category'),
    path('product-description/<slug:catogery_slug>/<slug:product_slug>/',views.product_description,name='product-description'),
    path('test/',views.product_list,name='test'),
]