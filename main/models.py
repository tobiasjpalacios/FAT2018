from django.db import models
from django.conf import settings


DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

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
        result = Classroom.objects.filter(retired=self)
        return result

    def getAppointments(self):
        result = Appointment.objects.filter(retired=self)
        return result
        
class Doctor(Person):
    speciality = models.CharField(max_length=32)
    
    def getDays(self):
        results = set()
        workdays = WorkDay.objects.filter(doctor=self)
        for a in workdays:
            if a.appointmentsAvailable():
                results.add(a)
        return results

    def daysAvailable(self):
        if self.getDays():
            return True
        return False
    
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
    retired = models.ForeignKey(Retired, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

class WorkDay(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField()

    def appointmentsAvailable(self):
        if Appointment.objects.filter(day=self, retired=None):
            return True
        return False

    def getAppointments(self):
        results = Appointment.objects.filter(day=self, retired=None)
        return results  
    
    def __str__(self):
        return "{}/{}".format(self.day.day, self.day.month)

class Classroom(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def getStudents(self):
        result = Enrrolment.objects.filter(classroom=self).retired
        return result
    
    def __str__(self):
        return "{}".format(self.name)

class ClassroomDay(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_CHOICES, default=False)
    start_hour = models.IntegerField()
    

class Affiliate(RelationRetired):
    pass    

class Partner(RelationRetired):
    pass

class Enrrolment(RelationParticipe):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.classroom, self.retired)

class Appointment(RelationParticipe):
    day = models.ForeignKey(WorkDay, on_delete=models.CASCADE)
    timeAttendance = models.TimeField()
    
    def __str__(self):
        return "{}:{}".format(self.timeAttendance.hour, self.timeAttendance.minute)