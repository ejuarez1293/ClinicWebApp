from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create Models


class Patient(models.Model):
    user = models.OneToOneField(User, related_name='user')  # might need to make this primary_key instead of id
    MALE = 1
    FEMALE = 2

    GENDERS = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    firstname = models.CharField(max_length=50, default='')
    lastname = models.CharField(max_length=50, default='')
    profilePic = models.ImageField(upload_to='profile_pics',
                                   blank=True, default=None)
    dateOfBirth = models.DateField(max_length=8, default='')
    ssn = models.CharField(max_length=9, unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    zip = models.IntegerField()
    gender = models.IntegerField(choices=GENDERS, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, default='')


    def __str__(self):
        return self.firstname + ' ' + self.lastname + ' ' + str(self.id)


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='Doctor')
    specialty = models.CharField(max_length=30)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Nurse(models.Model):
    user = models.OneToOneField(User, related_name='Nurse')
    specialty = models.CharField(max_length=30)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Recieptionist(models.Model):
    user = models.OneToOneField(User, related_name='Recieptionist', primary_key=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



class Appointment(models.Model):

    date = models.DateField()
    time = models.TimeField(null=True)
    patient = models.ForeignKey(Patient ,null = True)
    doctor = models.ForeignKey(Doctor)
    comments = models.CharField(max_length=2000)

    def __str__(self):
        return '%s by  %s' % (self.patient, self.doctor)


class Prescription(models.Model):
    date = models.DateField(null=True)
    patient = models.ForeignKey(Patient, null=True)
    doctor = models.ForeignKey(Doctor, null=True)
    medication = models.CharField(max_length=50)
    quantity = models.IntegerField()
    length = models.IntegerField()
    dosage = models.IntegerField()
    refill_count = models.IntegerField()





class Insurance(models.Model):
    patient = models.ForeignKey(Patient, null=True)
    doctor = models.ForeignKey(Doctor, null=True)
    companyName = models.CharField(max_length=50)
    contactNum = models.IntegerField()
    insID = models.IntegerField()
    insNetwork = models.BooleanField()

    def __str__(self):
        return self.companyName + str(self.insID)


class medicalChart(models.Model):

    date = models.DateField()
    patient = models.ForeignKey(Patient, null=True)
    doctor = models.ForeignKey(Doctor)
    reason_for_visit = models.TextField(max_length=250, default='')
    height = models.CharField(max_length=10, default='')
    weight = models.IntegerField()
    temperature = models.CharField(max_length=3,default='')
    pulse = models.CharField(max_length=10)
    blood_pressure=models.CharField(max_length=10,default='')
    diagnosis = models.TextField(max_length=250)
    additionalNotes = models.TextField(max_length=250)

class BillingLog(models.Model):

    patient = models.ForeignKey(Patient, null=True)
    procedure = models.CharField(max_length=100, default='')
    doctor = models.ForeignKey(Doctor, null=True)
    date = models.DateField(null=True)
    amount =  models.FloatField()

    def __str__(self):
        return '%s by  %s' % (self.patient, self.doctor)
