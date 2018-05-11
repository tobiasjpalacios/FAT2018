from django.forms import ModelForm
from .models import *

class ClassroomForm(ModelForm):
    model = Classroom
    fields = ['day','hour','capacity','duration','name','description']