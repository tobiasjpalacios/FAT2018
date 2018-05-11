from django.forms import ModelForm
from .models import *

class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ['day','hour','capacity','duration','name','description']

class DayForm(ModelForm)
	class Meta:
		model = Day
        fields = ['day', 'start_hour', 'finish_hour', 'interval']