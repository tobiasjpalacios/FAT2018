from django.forms import ModelForm
from .models import *
from django import forms
from django.conf import settings


DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

USER_TYPE_CHOICES = (
    (0, 'Jubilado'),
    (1, 'Doctor'),
    (2, 'Profesor')
)

class DayForm(forms.Form):
    start_hour = forms.TimeField(label='Hora de inicio')
    finish_hour = forms.TimeField(label='Hora de finalizacion')
    day = forms.ChoiceField(choices=DAYS_CHOICES)
    duration = forms.IntegerField()
    interval = forms.IntegerField()
    time_to_start = forms.IntegerField()    


class ClassRoomForm(forms.Form):
    name = forms.CharField(label ='Tu nombre', max_length=20)
    description = forms.CharField(label='descripcion',max_length=256)
    capacity = forms.IntegerField()

class ClassDayForm(forms.Form):
    day = forms.ChoiceField(choices=DAYS_CHOICES)
    start_hour =forms.IntegerField(label='hora de inicio')

class Registro(forms.Form):
    first_name = forms.CharField(label='nombre')
    last_name = forms.CharField(label='apellido')
    personal_id = forms.IntegerField(label='Documento')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    re_password = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput())
    email = forms.CharField(label='Correo electronico', required=False)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='tipo de usuario')

    
