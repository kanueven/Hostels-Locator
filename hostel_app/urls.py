from django.urls import path
from . import views

urlpatterns = [
	path('', views.hostel_home, name='hostel-home'),
	path('register/<str:role>/', views.registerView, name='register'),
	path('login/<str:role>/', views.loginView, name='login'),
	path('logout/', views.logoutView, name='logout'),
	path('hostels/', views.HostelListView.as_view(), name='hostel-list'),
	path('hostels/<int:pk>/', views.HostelDetailView.as_view(), name='hostel-detail'),
	#path('hostels/<int:pk>/book/', views.bookView, name='book'),
	path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/',views.profile,name='profile'),
]
