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
        form = Registro(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["personal_id"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            re_password = form.cleaned_data["re_password"]
            if password == re_password:
                if not User.objects.filter(username=username).exists():
                    new_user = User.objects.create_user(username, email, password)
                    new_user.is_active = False
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.save()
                    results["succeed"] = True
                    results['form'] = Registro()
                    return render(request, 'create_user.html', results)
                else:
                    results["username_Er"] = True
            else:
                results["password_Er"] = True
        results['form'] = form
    else :
        results['form'] = Registro()
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

def mLogOut(request):
    logout(request)
    return render(request, 'login.html')

def profile(request):
    results = {}
    try:
        retired = Retired.objects.get(user=request.user)
        return render(request, 'profile_for_retired.html')
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

def loadAppointments(request):
    results = {}
    results['doctor'] = Doctor.objects.get(id=request.GET.get('id'))
    return render(request, 'jquery_html/AppointmentInfo.html', results)

@require_POST
def requestAppointment(request):
    appointment = Appointment.objects.get(id=request.POST['id'])
    if appointment.retired == None:
        appointment.retired = Retired.objects.get(user=request.user)
        appointment.save()
        return HttpResponse("saved")
    return HttpResponse("Error")
    