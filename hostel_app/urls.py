from django.urls import path
from . import views

urlpatterns = [
	path('', views.hostel_home, name='hostel-home'),
	path('register/<str:role>/', views.registerView, name='register'),
	path('login/<str:role>/', views.loginView, name='login'),
	path('logout/', views.logoutView, name='logout'),
	path('hostels/', views.HostelListView.as_view(), name='hostel-list'),
    path('add_hostel/', views.HostelCreateView.as_view(), name='add-hostel'),
    path('add_services/<int:pk>/', views.add_services, name='add-services'),
    path('add_room/<int:pk>/', views.add_room, name='add-room'),
    path('add_hostelimage/<int:pk>/', views.add_hostelimages, name='add-images'),
	path('hostels/<int:pk>/', views.HostelDetailView.as_view(), name='hostel-detail'),
    path('booking/<int:pk>/', views.book_room, name='book-room'),
	path('confirm_booking/<int:pk>/', views.confirm_booking, name='confirm-booking'),
	path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/',views.profile,name='profile'),
]
