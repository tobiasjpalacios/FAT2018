from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import six 

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
    results['form'] = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            u = User()
            u.first_name=request.POST.get("first_name")
            u.last_name=request.POST.get("last_name")
            u.username=request.POST.get("username")
            u.email=request.POST.get("email")
            u.set_password(request.POST.get("password"))
            user_type = int(request.POST.get("user_type"))
            if user_type ==0:
                ut = Retired()
            elif user_type ==1:
                ut = Doctor()
            elif user_type ==2:
                ut = Teacher()
            u.save()
            ut.user=u
            ut.save()
            redirect(main)
        results['form'] = form
    return render(request, 'create_user.html', results)

def mLogIn(request):
    if not request.user.is_authenticated:
        results={}
        results["form"] = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
                if user is not None:
                    login(request, user)
                    return redirect(main)
            else:
                results["form"] = form
        return render(request, 'login.html', results)
    return redirect(main)

def mLogOut(request):
    logout(request)
    return redirect(mLogIn)

def profile(request):
    results = {}
    try:
        results['retired'] = Retired.objects.get(user=request.user)
        return render(request, 'profile_for_retired.html', results)
    except Retired.DoesNotExist:
        try:
            results['doctor'] = Doctor.objects.get(user=request.user)
            return render(request, 'profile_for_doctor.html', results)
        except Doctor.DoesNotExist:
            try:
                results['teacher'] = Teacher.objects.get(user=request.user)
                return render(request, 'profile_for_teacher.html', results)
            except:
                return HttpResponse("Tipo de usuario no identificado")

@require_GET
def loadAppointments(request):
    results = {}
    results['workdays'] = Doctor.objects.get(id=request.GET.get('doctor_id')).getDays()
    return render(request, 'jquery_html/AppointmentInfo.html', results)

@require_POST
def requestAppointment(request):
    appointment = Appointment.objects.get(id=request.POST['id'])
    if appointment.retired == None:
        appointment.retired = Retired.objects.get(user=request.user)
        appointment.save()
        return HttpResponse("OK")
    return HttpResponse("Error")

@require_POST
def deleteAppointment(request):
    appointment_id = request.POST.get('appointment_id')
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.retired = None
    appointment.save()
    return HttpResponse("OK")
    