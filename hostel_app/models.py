from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from hostel_app.admin import LocationAdmin
# Create your models here.


class Hostel(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='cover',default='default.png')
    services = models.ManyToManyField("Service")
    location = models.ForeignKey(LocationAdmin, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, null=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("hostel-detail", kwargs={"pk": self.pk})
    

    class Meta:
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        ordering = ['name']

class Room(models.Model):
    room_number = models.CharField(max_length= 10)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)


    def __str__(self) :
        return f"Room{self.room_number} - {self.capacity} beds"
    class Meta:
        ordering = ['room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()


class Category(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveIntegerField()
    hostel = models.ForeignKey("Hostel",  on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'UserLocation'
        verbose_name_plural = 'UserLocations'



class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
  
        
  

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default="guest", max_length=50)
    profile_pic = models.ImageField(
        upload_to='profile/', default='default.png')
    cover = models.ImageField(upload_to='cover/', default='default.png')
    age = models.PositiveSmallIntegerField(default=18)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.get_username()
    


class Review(models.Model):
    pass
