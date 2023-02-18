from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hostel(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='cover')
    services = models.ManyToManyField("Service")
    location = models.ForeignKey("Location", on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'


class Category(models.Model):
    name =models.CharField( max_length=50)
    cost =models.PositiveIntegerField()
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
    name = models.CharField( max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile/', default='profile/default.jpg')
    cover = models.ImageField(upload_to='cover/', default='cover/default.png')
    age = models.PositiveSmallIntegerField(default=18)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

  
    

    def __str__(self):
        return self.get_username()


class Review(models.Model):
    pass
