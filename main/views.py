from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import six
from django.utils.dateparse import parse_time


# Create your views here.
def main(request):
    results = {}
    return render(request, 'main.html', results)
    
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
            login(request, u)
            results["message"] = True
            results["message_text"] = "{} tu usuario ha sido creado".format(u.first_name)
            return render(request, 'main.html', results)
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
                    results["message"] = True
                    results["message_text"] = "{} has sido logueado".format(user.first_name)
                    return render(request, 'main.html', results)
            else:
                results["form"] = form
        return render(request, 'login.html', results)
    return redirect(main)

def mLogOut(request):
    results = {}
    results["message"] = True
    results["message_text"] = "{} has sido deslogueado".format(request.user.first_name)
    logout(request)
    return render(request, 'main.html', results)    

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
    results['workdays'] = Doctor.objects.get(id=request.GET.get('doctor_id')).daysAvailable()
    return render(request, 'jquery_html/AppointmentInfo.html', results)

@require_POST
def requestAppointment(request):
    appointment = Appointment.objects.get(id=request.POST['id'])
    if appointment.retired == None:
        appointment.retired = Retired.objects.get(user=request.user)
        appointment.save()
        results = {}
        results['doctors'] = Doctor.objects.all()
        results["message"] = True
        results["message_text"] = "se ha solicitado un turno para el {}".format(appointment.workday.day)
        return render(request, 'appointment.html', results)
    return HttpResponse("Error")

@require_POST
def deleteAppointment(request):
    appointment_id = request.POST.get('appointment_id')
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.retired = None
    appointment.save()
    return HttpResponse("OK")
    
@require_GET
def loadWorkDayForm(request):
    results={}
    results['form'] = WorkDayForm()
    return render(request, 'jquery_html/WorkDayForm.html', results)

@require_POST
def addWorkDayForm(request):
    results = {}
    results['doctor'] = Doctor.objects.get(user=request.user)
    form = WorkDayForm(request.POST)
    if form.is_valid():
        day = request.POST.get('day')
        workday, created = WorkDay.objects.get_or_create(doctor=results['doctor'], day=day)
        start_min = toMinutes(parse_time(request.POST.get('start_hour')))
        finish_min = toMinutes(parse_time(request.POST.get('finish_hour')))
        duration = toMinutes(parse_time(request.POST.get('duration'))) + toMinutes(parse_time(request.POST.get('interval')))
        while start_min < finish_min:
            hour = toTime(start_min)
            appointment = Appointment(workday=workday, timeAttendance=hour)
            appointment.save()
            start_min +=duration
        return redirect(profile)
    results['form'] = form
    return render(request, 'profile_for_doctor.html', results)

@require_POST
def deleteWorkDay(request):
    workday_id = request.POST.get('workday_id')
    workday = WorkDay.objects.get(id=workday_id).delete()
    return HttpResponse("OK")



def toMinutes(time):
    minute = time.minute
    hours = time.hour
    while hours > 0:
        minute += 60
        hours -= 1
    return minute

def toTime(time):
    minute = time
    hour = 0
    while minute >= 60:
        hour += 1
        minute -= 60
    return datetime.time(hour, minute)