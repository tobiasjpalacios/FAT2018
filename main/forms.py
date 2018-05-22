from django.forms import ModelForm
from .models import *
from django import forms

class DayForm(forms.Form):
    start_hour = forms.TimeField(label='Hora de inicio')
    finish_hour = forms.TimeField(label='Hora de finalizacion')
    day = forms.IntegerField()
    duration = forms.IntegerField()
    interval = forms.IntegerField()
    time_to_start = forms.IntegerField()    