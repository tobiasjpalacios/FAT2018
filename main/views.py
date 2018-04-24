from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User

# Create your views here.
def main(request):
    return render(request, 'main.html')
    
def classrooms(request):
    return render(request, 'classrooms.html')

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
    return render(request, 'login.html')