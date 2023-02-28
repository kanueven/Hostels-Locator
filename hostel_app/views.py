from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from hostel_app.forms import LoginForm, UserForm, HostelForm
from .models import Hostel, Location


def hostel_home(request):
    context = {}
    context['hostels'] = Hostel.objects.all()
    return render(request, 'hostel_home.html', context)


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

def profile(request):
    return render(request, 'profile.html')

class HostelListView(generic.ListView):
    model = Hostel
    template_name = "hostel_list.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context['locations'] = Location.objects.all()
        context['select_location'] = self.request.GET.get("location")
        if query:
            context["query"] = query
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        location = self.request.GET.get("location")
        if query:
            queryset = queryset.filter(name__icontains=query)
            
        if location:
            queryset = queryset.filter(location__name__icontains=location)
            
        return queryset
    


class HostelDetailView(generic.DetailView):
    model = Hostel
    template_name = "hostel_detail.html"


def registerView(request, role):
    context = {}
    context['role'] = role
    if request.method == 'POST':
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
                context['usererror'] = get_user_model().objects.filter(
                    username=form.cleaned_data['username'])
                context['errors'] = True
            else:
                return redirect('hostel-home')

    return render(request, 'login.html', context=context)


def logoutView(request):
    logout(request)
    return redirect('hostel-home')
