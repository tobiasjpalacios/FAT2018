from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_POST

# Create your views here.
def main(request):
    return render(request, 'main.html')
    
def classrooms(request):
    results={}
    now = datetime.datetime.now()
    results['clases'] = ClassroomDay.objects.all()
    results['days'] = DAYS_CHOICES
    print("{}".format(DAYS_CHOICES[now.weekday()]))
    print("{} {}/{}".format(now.strftime("%A"), 25, now.month))
    return render(request, 'classroom.html', results)

def appointments(request):
    results = {}
    results['doctors'] = Doctor.objects.all()
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
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def loadAppointments(request):
    results = {}
    results['doctor'] = Doctor.objects.get(id=request.GET.get('id'))
    return render(request, 'AppointmentInfo.html', results)

@require_POST
def requestAppointment(request):
    appointment = Appointment.objects.get(id=request.POST['id'])
    if appointment.retired == None:
        appointment.retired = Retired.objects.get(user=request.user)
        appointment.save()
        return HttpResponse("saved")
    return HttpResponse("Error")
    