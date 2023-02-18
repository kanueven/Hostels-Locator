from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Hostel(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='cover',default='default.png')
    services = models.ManyToManyField("Service")
    location = models.ForeignKey(
        "Location", on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, null=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("hostel-detail", kwargs={"pk": self.pk})
    

    class Meta:
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'


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
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


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
