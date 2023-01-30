from django.shortcuts import render

# Create your views here.

def base_homepage(request):
   

  
    return render(request, 'homepage.html')