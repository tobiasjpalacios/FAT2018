from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Person)
admin.site.register(Work_day)
admin.site.register(Appointment)
admin.site.register(Classroom)
admin.site.register(Classroom_day)
admin.site.register(Classroom_place)
admin.site.register(Enrolment_teacher)
admin.site.register(Enrolment_student)
