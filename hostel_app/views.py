from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from hostel_app.forms import LoginForm, UserForm, HostelForm
from .models import Hostel, Location


def hostel_home(request):
    context = {}
    context['hostels'] = Hostel.objects.all()
    return render(request, 'hostel_home.html',context)


@login_required(login_url='login')
def dashboard(request):
    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.owner = request.user  # add the owner field
            hostel.save()
            return HttpResponseRedirect(reverse('hostel-detail', args=[str(hostel.id)]))
    else:
        form = HostelForm()

    context = {}
    context['locations'] = Location.objects.all()
    context['hostels'] = Hostel.objects.filter(
        owner=request.user)  # filter hostels by owner
    context['form'] = form

    return render(request, 'dashboard.html', context)



class HostelListView(generic.ListView):
    model = Hostel
    template_name = "hostel_list.html"


class HostelDetailView(generic.DetailView):
    model = Hostel
    template_name = "hostel_detail.html"


def registerView(request, role):
    context = {}
    context['role'] = role
    if request.method == 'POST':
        print('1')
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=True)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)

            return redirect('hostel-home')

    context['form'] = UserForm()

    return render(request, 'register.html', context=context)


def loginView(request, role):
    if request.user.is_authenticated:
        return redirect('hostel-home')
    context = {}
    context['role'] = role
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = form.clean()
            try:
                new_user = authenticate(
                    username=form.cleaned_data['username'], password=form.cleaned_data['password'],)
                login(request, new_user)

            except:

                context['errors'] = True
            else:
                return redirect('hostel-home')

    return render(request, 'login.html', context=context)


def logoutView(request):
    logout(request)
    return redirect('hostel-home')
