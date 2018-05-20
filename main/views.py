from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import *
import datetime

# Create your views here.
def main(request):
    return render(request, 'main.html')
    
def classrooms(request):
    results={}
    now = datetime.datetime.now()
    results['clases']=Classroom.objects.filter(day__gte=now.date())
    return render(request, 'classroom.html', results)

def appointments(request):
    results = {}
    now = datetime.datetime.now()
    results['turnos'] = Day.objects.filter(day__gte=now.date())
    return render(request, 'appointment.html', results)

def teachers(request):
    return render(request, 'teachers.html')

def days(request):
    return render(request, 'days.html')

def createuser(request):
    results={}
    if request.method == "POST":
        username = request.POST["personalid"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if password == repassword:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            retired = Retired.objects.create(user=user)
            retired.save()
            return redirect(main)
    return render(request, 'create_user.html')

def mLogIn(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return redirect(main)

def mLogOut(request):
    logout(request)

def profile(request):
    return render(request, 'profile.html')