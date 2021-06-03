from django.urls import path
from . import views

urlpatterns = [

    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('sub_cart/<int:product_id>/',views.sub_product,name='sub_product'),
    path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('checkout',views.checkout,name='checkout'),
]