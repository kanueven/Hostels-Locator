from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView,TemplateView,FormView
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from hostel_app.forms import LoginForm, UserForm, HostelForm
from .models import Hostel, Location,Room,Book


#create a view in Django that accepts location data via POST request and saves it to the database

class LiveLocationView(TemplateView):
    template_name = 'live_location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = Location.objects.get(pk=self.kwargs['pk'])
        context['location'] = location
        return context
    

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
    
def add_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hostel_list')
    else:
        form = HostelForm()
    return render(request, 'add_hostel.html', {'form': form})

class HostelDetailView(DetailView):
    model = Hostel
    template_name = "hostel_detail.html"

def hostel_detail(request, hostel_id):
    hostel = Hostel.objects.get(id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)
    return render(request, 'hostel_detail.html', {'hostel': hostel, 'rooms': rooms})

def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    bookings = Book.objects.filter(room=room)
    return render(request, 'room_detail.html', {'room': room, 'bookings': bookings})
#one for displaying the details of a specific hostel and its rooms, 
# and one for displaying the details of a specific room and its bookings
class BookHostelView(FormView):
    template_name = 'book_hostel.html'
    form_class = BookingForm

    def get_success_url(self):
        return reverse('booked_hostel', kwargs={'hostel_id': self.kwargs['hostel_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hostel'] = Hostel.objects.get(pk=self.kwargs['hostel_id'])
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



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

