
from django.forms import ModelForm
from .models import *

class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ['capacity','name','description']

class WorkDayForm(ModelForm):
    class Meta:
        model = WorkDay
        fields = ['day' ]