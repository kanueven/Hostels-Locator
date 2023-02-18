from django.shortcuts import render,redirect
from .forms import HostelForm
from django.views.generic import ListView
from .models import Hostel
# Create your views here.


def base_homepage(request):
    form = HostelForm()
    return render(request, 'homepage.html',{'form':form})

class HostelListView(ListView):
    model = Hostel

def signup(request):
    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(redirect_to)
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=True)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)

            return redirect(redirect_to)
    context['form'] = UserForm()
    context['redirect_to'] = redirect_to if redirect_to else 'hostel_base'

    return render(request, 'sign_up.html', context=context)


def signin(request):
    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(redirect_to)
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            new_user = form.clean()
            try:
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        )

                login(request, new_user)
            except:
                context['errors'] = True
            else:
                return redirect(redirect_to)
    context['form'] = LoginForm()
    context['redirect_to'] = redirect_to if redirect_to else 'hostel_base'

    return render(request, 'sign_in.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponse("success")