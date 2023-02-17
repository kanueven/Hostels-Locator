from django.shortcuts import render
from .forms import HostelForm
from django.views.generic import ListView
from .models import Hostel
# Create your views here.


def base_homepage(request):
    form = HostelForm()
    return render(request, 'homepage.html',{'form':form})

class HostelListView(ListView):
    model = Hostel