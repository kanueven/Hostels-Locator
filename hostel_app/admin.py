from django.contrib import admin
from .models import Booking, Hostel, Location, RoomCategory, Service, UserProfile, Review

# Register your models here.


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'location')
    search_fields = ('name', 'address', 'location__name')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ('room',)
    search_fields = ('room__name', 'room__hostel__name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'user__email')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display=('hostel',)
