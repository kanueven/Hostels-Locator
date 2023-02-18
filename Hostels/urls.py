from django.urls import path
from . import views



urlpatterns = [
    path('', views.base_homepage, name='base_homepage'),
    path('hostels/',views.HostelListView.as_view(),name='hostel-list'),
    path('sign-in/', views.signin, name='signin'),
    path('sign-up/', views.signup, name='signup'),
]