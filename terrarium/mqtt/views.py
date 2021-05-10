from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from . import mqtt
from .models import Humidity


# Create your views here.

def index(request):
    # if not logged in go back to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # if logged in go to index
    return render(request, 'mqtt/index.html')


def login_view(request):
    # check if user submitted username and password
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # check if user exists (authentication)
        user = authenticate(request, username=username, password=password)

        # if user found then log in and go to index page otherwise stay on login page and display error
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'mqtt/login.html', {"error": "User not found"})

    return render(request, 'mqtt/login.html')


def register_view(request):
    # registration form processing
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST["cpassword"]

        # password and confirm password should be equal
        if password != cpassword:
            return render(request, 'mqtt/register.html', {
                'error': 'passwords must match'
            })

        # Try to create a new user (register) - this will throw an exception if the user already has an account
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return render(request, 'mqtt/login.html', {
                "success_message": "User account created. Please login"
            })

        except IntegrityError:
            return render(request, 'mqtt/register.html', {
                "error": "Username already taken"
            })

    return render(request, 'mqtt/register.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# profile page view


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Update profile - TODO
        try:
            user = request.user
            user.first_name = fname
            user.last_name = lname
            user.username = username
            user.password = password
            user.save()
        except Exception as e:
            print(str(e))
            return render(request, 'mqtt/profile.html', {
                "profile": profile,
                "error": "Could not save profile"

            })

        return HttpResponseRedirect(reverse('profile'))

    profile = {
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "username": request.user.username,
        "email": request.user.email,
        "password": request.user.password
    }

    return render(request, 'mqtt/profile.html', {
        "profile": profile

    })


def define_rate_view(request):
    # if not logged in go back to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'mqtt/define_rate.html')


def bibliotheque_view(request):
    # if not logged in go back to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # Add new record from form on library page and save values in the db
    if request.method == "POST":
        name = request.POST['name']
        min_rate = request.POST['minRate']
        max_rate = request.POST['maxRate']

        if min_rate >= max_rate:
            humidityRecords = Humidity.objects.all()
            return render(request, 'mqtt/bibliotheque.html', {
                "humidityRecords": humidityRecords,
                "error": "Min rate cannot be greater than max rate"
            })

        try:
            hum = Humidity(name=name, min_rate=min_rate, max_rate=max_rate)
            hum.save()
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse('bibliotheque'))

    humidityRecords = Humidity.objects.all()
    return render(request, 'mqtt/bibliotheque.html', {
        "humidityRecords": humidityRecords
    })

# this page displays the control slider and makes the connection to mqtt
# library page sends min and max values to it through GET
# define_rate page sends info to it through POST when you press SET button


def control_view(request):
    # if not logged in go back to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        min_rate = request.POST['minRate']
        max_rate = request.POST['maxRate']

        data = {
            "min_rate": min_rate,
            "max_rate": max_rate
        }
        return render(request, 'mqtt/control.html', {
            "data": data
        })
    else:
        print(request.GET)
        if len(request.GET) != 0:
            min_rate = request.GET['min']
            max_rate = request.GET['max']

            data = {
                "min_rate": min_rate,
                "max_rate": max_rate
            }
            return render(request, 'mqtt/control.html', {
                "data": data
            })

        return render(request, 'mqtt/control.html')
