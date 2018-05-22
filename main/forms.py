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


class DayForm(forms.Form):
    start_hour = forms.TimeField(label='Hora de inicio')
    finish_hour = forms.TimeField(label='Hora de finalizacion')
    day = forms.IntegerField(widget =forms.SelectDateWidget (DAYS_CHOICES))
    duration = forms.IntegerField()
    interval = forms.IntegerField()
    time_to_start = forms.IntegerField()    


class ClassRoomForm(forms.Form):
    name = forms.CharField(label ='Tu nombre', max_length=20)
    description = forms.CharField(label='descripcion',max_length=256)
    capacity = forms.IntegerField()

class ClassDayForm(forms.Form):
    day = forms.IntegerField(widget=forms.SelectDateWidget(DAYS_CHOICES))
    start_hour =forms.IntegerField(label='hora de inicio')