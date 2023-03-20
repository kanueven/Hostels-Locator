from django import forms
from django.shortcuts import redirect,render
from .models import Hostel, Location,Book,Room
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
        model = Book
        fields = ['room', 'start_date', 'end_date', 'guest_name', 'guest_email']

def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = BookingForm()
    return render(request, 'book_room.html', {'form': form, 'room': room})




class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()



