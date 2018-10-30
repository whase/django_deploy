from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from appsix.forms import UserProfileInfoForm, UserForm

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    my_dict = {'my_title':'index'}
    return render(request, 'appsix/index.html',context=my_dict)

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'appsix/register.html', {'my_title':"register",'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("account inactive")
        else:
            print("someone tried to log in and failed")
            return HttpResponse("invalid login details")
    else:
        return render(request,'appsix/index.html', {"my_title":"index"})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
