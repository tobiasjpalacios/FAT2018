from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('profile/', profile, name='profile'),
    path('appointments/', appointments, name='appointments'),
    path('classrooms/', classrooms, name='classrooms'),
    path('teachers/', teachers, name='teachers'),
    path('createuser/', createuser, name='createuser'),
    path('mlogin/', mLogIn, name='mLogIn'),
    path('mlogout/', mLogOut, name='mLogOut'),
    path('loadAppointments/', loadAppointments, name='loadAppointments'),
    path('requestAppointment/', requestAppointment, name='requestAppointment'),
    path('deleteAppointment/', deleteAppointment, name='deleteAppointment'),
]