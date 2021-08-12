from django.urls import path
from . import views

urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('test', views.test, name='test'),
    path('razorpay_payment/<str:order_no>',
         views.razorpay_payment, name='razorpay_payment'),
]
