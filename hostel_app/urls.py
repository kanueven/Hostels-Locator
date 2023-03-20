from django.urls import path
from . import views

urlpatterns = [
	path('', views.hostel_home, name='hostel-home'),
	path('register/<str:role>/', views.registerView, name='register'),
	path('login/<str:role>/', views.loginView, name='login'),
	path('logout/', views.logoutView, name='logout'),
	path('hostels/', views.HostelListView.as_view(), name='hostel-list'),
    path('add_hostel/', views.add_hostel, name='add_hostel'),

	path('hostels/<int:pk>/', views.HostelDetailView.as_view(), name='hostel-detail'),

    path('live_location/<int:pk>/', views.LiveLocationView.as_view(), name='live_location'),
    path('book_hostel/<int:hostel_id>/', views.BookHostelView.as_view(), name='book_hostel'),
	#path('hostels/<int:pk>/book/', views.bookView, name='book'),
	path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/',views.profile,name='profile'),
]
