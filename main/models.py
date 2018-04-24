from django.db import models
from django.conf import settings

class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    personalID = models.IntegerField(unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        abstract = True

class Retired(Person):
    def isAffiliate(self):
        if Affiliate.objects.get(retired=self):
            return True
        return False
    
    def isPartner(self):
        if Partner.objects.get(retired=self):
            return True
        return False
    
    def getClassrooms(self):
        return False

    def getAppointments(self):
        result = Appointment.objects.filter(retired=self)
        return result
        
class Doctor(Person):
    speciality = models.CharField(max_length=32)
    
    def getDays(self):
        results = Day.objects.filter(doctor=self)
        return results

class Teacher(Person):
    subject = models.CharField(max_length=32)
    
    def getClassrooms(self):
        my_Classrooms = Classroom.objects.filter(teacher=self)
        return my_Classrooms


class RelationRetired(models.Model):
    number = models.IntegerField()
    retired = models.OneToOneField(Retired, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.number, self.retired)

    class Meta:
        abstract = True

class RelationParticipe(models.Model):
    retired = models.ForeignKey(Retired, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Day(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField(auto_now=False)
    start_hour = models.DateTimeField(auto_now=False)
    finish_hour = models.DateTimeField(auto_now=False)
    interval = models.IntegerField()

    def getAppointments(self):
        results = Appointment.objects.filter(dat=self).retired
        return results

class Classroom(models.Model):
    day = models.DateField(auto_now=False)
    hour = models.DateTimeField(auto_now=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    duration = models.IntegerField()

    def getStudents(self):
        result = Enrrolment.objects.filter(classroom=self).retired
        return result

class Affiliate(RelationRetired):
    pass    

class Partner(RelationRetired):
    pass

class Enrrolment(RelationParticipe):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.classroom, self.retired)

class Appointment(RelationParticipe):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    timeAttendance = models.TimeField()
    
    def __str__(self):
        return "{} - {}".format(self.day, self.retired)