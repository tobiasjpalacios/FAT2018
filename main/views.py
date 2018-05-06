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

    return render(request, 'classrooms.html', results)

def teachers(request):
    return render(request, 'teachers.html')

def days(request):
    return render(request, 'days.html')

def createuser(request):
    results={}
    if request.method == "POST":
        form= RetiredForm(request.POST)
        if form.is_valid():
            instance = form.instance
            password=request.POST['password']
            repassword=request.POST['repassword']
            if password == repassword:
                if not User.objects.filter(username=instance.personalID).exists():
                    user = User.objects.create_user(instance.personalID, instance.email, password)
                    instance.user = user
                    instance.save()
                    #user.first_name = instance.first_name
                    #user.last_name = instance.last_name
                    #user.save()
                    return redirect(main)
                else:
                    results["error_user"]= True
            else:
                results['error_password']=True
    results['form']=RetiredForm()
    return render(request, 'create_user.html', results)

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