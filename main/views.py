from django.shortcuts import render

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
    return render(request, 'create_user.html')