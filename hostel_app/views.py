from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from hostel_app.forms import HostelImageForm, LoginForm, RoomCategoryForm, UserForm, HostelForm
from .models import Booking, Hostel, Location, RoomCategory, UserProfile, Service, User


# create a view in Django that accepts location data via POST request and saves it to the database

##################################################################################
####################### Hostel Views            ##################################
##################################################################################


def hostel_home(request):
    context = {}
    context['hostels'] = Hostel.objects.all()
    return render(request, 'hostel_home.html', context)


class HostelCreateView(LoginRequiredMixin, generic.CreateView):
    model = Hostel
    form_class = HostelForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class HostelListView(generic.ListView):
    model = Hostel
    template_name = "hostel_list.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        lat = self.request.GET.get("lat")
        long = self.request.GET.get("lng")
        nearby = self.request.GET.get("nearby")
        try:
            user_location = get_location(lat, long)
            context['show_near'] = nearby
            context['nearby'] = Hostel.objects.filter(
                location__name__icontains=user_location)
            context['user_location'] = user_location
        except:
            pass
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


class HostelDetailView(DetailView):
    model = Hostel
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['room_form'] = RoomCategoryForm()
        context['image_form'] = HostelImageForm()
        if self.request.user.is_authenticated:
            context["owner"] = Hostel.objects.filter(owner=self.request.user)
            context['guest'] = Booking.objects.filter(user=self.request.user,room__hostel__id = self.kwargs['pk'])
        return context
    

def get_location(lat, long):
    import geocoder
    g = geocoder.osm([lat, long], method='reverse')
    return g.json['state']


def add_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hostel_list')
    else:
        form = HostelForm()
    return render(request, 'add_hostel.html', {'form': form})

def add_services(request,pk):
    if request.method == 'POST':
        hostel = Hostel.objects.get(id=pk)
        for k,v in request.POST.items():
            if k == 'csrfmiddlewaretoken':
                continue
            else:
                id = k[-1]
                services = Service.objects.get(id=id)
                hostel.services.add(services)
        
        hostel.save()
                
        return redirect('hostel-detail',pk)
    
def add_room(request,pk):
    if request.method == 'POST':
        form = RoomCategoryForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = Hostel.objects.get(id=pk)
            room.save()
            return redirect('hostel-detail',pk)
        
def add_hostelimages(request,pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    if request.method == 'POST':
        form = HostelImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.hostel = hostel  # Associate the image with the hostel
            image.save()
            return redirect('hostel-detail', pk=pk)
        

# def hostel_detail(request, hostel_id):
#     hostel = Hostel.objects.get(id=hostel_id)
#     rooms = Room.objects.filter(hostel=hostel)
#     return render(request, 'hostel_detail.html', {'hostel': hostel, 'rooms': rooms})


# def room_detail(request, room_id):
#     room = Room.objects.get(id=room_id)
#     bookings = Booking.objects.filter(room=room)
#     return render(request, 'room_detail.html', {'room': room, 'bookings': bookings})

# one for displaying the details of a specific hostel and its rooms,
# and one for displaying the details of a specific room and its bookings

#manage guests

def admin_report(request):
    num_hostels = Hostel.objects.count()
    num_guests = User.objects.count()
    context = {'num_hostels': num_hostels, 'num_guests': num_guests}
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def dashboard(request):
    context = {}
    if request.user.userprofile.role == 'guest':
        return render(request, 'profile.html')

    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.owner = request.user  # add the owner field
            hostel.save()
            return HttpResponseRedirect(reverse('hostel-detail', args=[str(hostel.id)]))
    else:
        form = HostelForm()
        
    num_guests = User.objects.count()
    num_hostels = Hostel.objects.count()
    context = {'num_guests': num_guests, 'num_hostels': num_hostels}
 

    context['locations'] = Location.objects.all()
    context['hostels'] = Hostel.objects.filter(
        owner=request.user)  # filter hostels by owner
    context['form'] = form

    return render(request, 'dashboard.html', context)


def profile(request):
    return render(request, 'profile.html')


def book_room(request,pk):
    room = RoomCategory.objects.get(id=pk)
    booked = request.GET.get('booked')
    if booked:
        booking = Booking.objects.create(user=request.user, room=room, start_date=datetime.today(
        ).date(), end_date=datetime.today().date())
        booking.save()
        return redirect('hostel-detail',pk=room.hostel.id)
    return render(request,'book_room.html',{'pk':pk,'category':room})

@login_required(login_url='login')
def confirm_booking(request,pk):
    if request.method == 'POST':
        room = RoomCategory.objects.get(id=pk)
        user = request.user
        print(request.POST['start_date'])
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        booking = Booking.objects.create(room=room,user=user,start_date=start,end_date=end)
        booking.save()
        return redirect('hostel-detail',room.hostel.id)


def registerView(request, role):
    context = {}
    context['role'] = role
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=True)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)

            if new_user is not None:
                # Create userprofile
                user_profile = UserProfile.objects.create(
                    user=new_user, role=role)
                user_profile.save()
                login(request, new_user)

            return redirect('hostel-home')
        else:
            context['form'] = form
    else:
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
