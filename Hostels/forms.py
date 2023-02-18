from django import forms
from .models import Hostel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class HostelForm(forms.ModelForm):
    
    class Meta:
        model = Hostel
        fields = ("name","cover")

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'inputGroupPrepend', 'placeholder': 'JohnDoe'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        }
        

def validate_username(username):
    pass
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'JohnDoe'}),help_text="Your profile username")
    password = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'password', 'class': 'form-control', 'aria-describedby': 'passHelp'}))

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False
        return True
    
