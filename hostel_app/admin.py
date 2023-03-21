from django.contrib import admin
from .models import Booking, Hostel, Room, Category, Location, Service, UserProfile, Review

# Register your models here.


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'location')
    search_fields = ('name', 'address', 'location__name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'hostel')
    search_fields = ('name', 'hostel__name')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ('room',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'location')
    search_fields = ('user__username', 'user__email')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
