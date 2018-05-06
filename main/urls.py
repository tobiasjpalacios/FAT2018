from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('profile/', profile, name='profile'),
    path('appointments/', appointments, name='appointments'),
    path('classrooms/', classrooms, name='classrooms'),
    path('teachers/', teachers, name='teachers'),
    path('createuser/', createuser, name='createuser'),
    path('mlogin/', mLogIn, name='mLogIn'),
]