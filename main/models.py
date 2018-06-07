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

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user-tipe= models.IntegerField()
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name, self.user-tipe)

class WorkDay(models.Model):
    doctor = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()



    def __str__(self):
        return "{}/{}".format(self.day.day, self.day.month)

class Classroom(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    duration=models.CharField(max_length=256)


    def __str__(self):
        return "{}".format(self.name, )

class Classroom_day(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = models.IntegerField()


class Classroom_place(models.Model):
    salon=models.IntegerField()
    capacity=models.IntegerField()
    classroom=models.ForeignKey(Classroom, on_delete=models.CASCADE)


class Enrrolment(RelationParticipe):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person=models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        classroomDay = self.nextDay()
        if classroomDay:
            return "{} {}".format(self.classroom.name, classroomDay.day)
        return "{} - {}".format(self.classroom.name, "No hay fechas disponibles")

class Appointment(RelationParticipe):
    workday = models.ForeignKey(WorkDay, on_delete=models.CASCADE)
    timeAttendance = models.TimeField()
    
    def __str__(self):
        return "{}".format(self.timeAttendance)
class E_teacher(Person):


class E_student(Person):
