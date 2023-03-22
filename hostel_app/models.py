from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your models here.


class Hostel(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='cover', default='default.png')
    services = models.ManyToManyField("Service")
    location = models.ForeignKey(
        'Location', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hostel-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        ordering = ['name']


class Room(models.Model):
    #Django will automatically generate a dropdown menu for the category field with the three options defined in ROOM_CATEGORY. When a user selects an option and submits the form,
    #  Django will store the short code for the selected category in the category field.
    ROOM_CATEGORY = (
        ['YAC', 'AC'],
        ['DEL', 'DELUKE'],
        ['QUE', 'QUEEN'],
    )

    room_number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORY)
    capacity = models.IntegerField()
    beds = models.IntegerField()
  

    def __str__(self):
        return f'{self.room_number}. {self.category} with{self.beds}beds for {self.capacity} people'

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f" {self.user}has booked {self.room} from {self.start_date} to {self.end_date}"
  




class Location(models.Model):
    
    name = models.CharField(max_length=150,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

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
