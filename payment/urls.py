# dj_razorpay/urls.py

from django.urls import path
from payment import views

urlpatterns = [
	path('', views.homepage, name='payment'),
	path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]