from django.db import models
from django.conf import settings
import datetime
from django.db.models import Q

DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

USER_CHOICES = (
    (0, 'jubilado'),
    (1, 'doctor'),
    (2, 'profesor'),
    (3, 'administrador'),
)
class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type= models.IntegerField(choices=USER_CHOICES)


class Work_day(models.Model):
    doctor = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()
    
    def get_appoiment(self, person_fill):
        results = Appointment.objets.filter(workday=self, person__isnull=person_fill)
        return results

    def appointment_available(self):
        availables = self.getappoiment(True).count()
        if availables == 0:
            return False
        return True 

class Classroom(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    duration = models.CharField(max_length=256)
    
    def get_classroom_days(self):
        results = Classroom_day.objets.filter(clasroom=self)
        return results

    def get_classroom_place(self):
        result = Classroom_place.objects.get(classroom=self)
        return result
    
    def get_next_day(self):
        classroom_days = self.get_classroom_days()
        for classroom_day in classroom_days:
            if classroom_day >= datetime.datetime.today().weekday():
                return classroom_day
        return classroom_days.first()


class Classroom_day(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_CHOICES)
    start_hour = models.TimeField()


class Classroom_place(models.Model):
    room = models.IntegerField()
    capacity = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)


class RelationParticipe(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Enrolment(RelationParticipe):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class Appointment(RelationParticipe):
    work_day = models.ForeignKey(Work_day, on_delete=models.CASCADE)
    time_attendance = models.TimeField()
    authorized = models.BooleanField(default=False)

class Enrolment_teacher(Enrolment):
    pass


class Enrolment_student(Enrolment):
    pass