from django import forms
from .models import Hostel, Location
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


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
