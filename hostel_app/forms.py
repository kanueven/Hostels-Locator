from django import forms
from django.shortcuts import redirect,render
from .models import Hostel, Location,Booking,Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class HostelForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hostel Name'}), label='Name *')
    cover = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control'}), label='Cover *')
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hostel Address'}), label='Address *')
    location = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'form-select', 'autofocus': ''}), queryset=Location.objects.all(), empty_label="Pick a city", label='Location *')

    class Meta:
        model = Hostel
        fields = ("name", "cover", "address", "location")

#Create forms for creating and updating bookings
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date', ]
        room = forms.ModelChoiceField(queryset=Room.objects.all())
        start_date = forms.DateField()
        end_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

def book_room(room, check_in, check_out, user):
    booking = Booking.objects.create(room=room, check_in=check_in, check_out=check_out, user=user)
    room.bookings.add(booking)
    room.save()



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()



