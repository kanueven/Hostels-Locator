from django.template.loader import render_to_string
from django.core.mail import send_mail
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


class RoomCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_rooms_left(self):
        return self.quantity - self.booking_set.count()

    class Meta:
        verbose_name = 'Room_category'
        verbose_name_plural = 'Room_categories'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    room = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):

        # Send email to the user
        subject = 'Booking confirmation'
        from_email = 'from@example.com'
        html_message = render_to_string('booking_confirmation_email.html', {
            'room': self.room, 'user': self.user, 'start_date': self.start_date, 'end_date': self.end_date})
        recipient_list = [self.user.email]
        send_mail(subject, message=None, html_message=html_message,
                  from_email=from_email, recipient_list=recipient_list)

        return super().save(*args, **kwargs)


    def __str__(self):
        return f" {self.user}has booked {self.room} from {self.start_date} to {self.end_date}"


class Location(models.Model):
    name = models.CharField(max_length=150, blank=True)

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


class HostelImage(models.Model):
    image= models.ImageField(upload_to='images/')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'HostelImage'
        verbose_name_plural = 'HostelImages'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default="guest", max_length=50)
    profile_pic = models.ImageField(
        upload_to='profile/', default='default.png')
    cover = models.ImageField(upload_to='cover/', default='default.png')
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.get_username()


class Review(models.Model):
    pass
