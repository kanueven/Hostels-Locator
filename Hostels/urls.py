from django.urls import path
from . import views



urlpatterns = [
    path('', views.base_homepage, name='base_homepage'),
    path('hostels/',views.HostelListView.as_view(),name='hostel-list'),
]