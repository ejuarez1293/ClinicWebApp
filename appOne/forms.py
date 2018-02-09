from django import forms
from .models import Appointment

from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Patient
from .models import Doctor
from .models import Insurance
from .models import medicalChart
from .models import Prescription
from .models import BillingLog




# class ProfileForm(ModelForm):
#    class Meta:
#        model = Profile


class LoginForm(forms.Form):
	username = forms.CharField(label='User Name', max_length=64)
	password = forms.CharField(label="Password ", widget=forms.PasswordInput())

class PostAppointment(forms.Form):
	
	date = forms.DateField(label="date")
	time = forms.TimeField(label="time")
	patient = forms.IntegerField(label="patient")
	doctor = forms.IntegerField(
		widget=forms.Select(
			choices= Doctor.objects.all().values_list('id',"user__first_name")
		)
	)
	comments = forms.CharField(label="comments", max_length=2000)

class PostBill(forms.Form):
	date = forms.DateField(label="date")
	patient = forms.IntegerField(label="patient")
	procedure = forms.CharField(label="procedure")
	amount = forms.FloatField(label="amount")
	doctor = forms.IntegerField(
		widget=forms.Select(
			choices = Doctor.objects.all().values_list('id',"user__first_name")
		)
	)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class PatientProfileInfoForm(forms.ModelForm):
	class Meta:
		model = Patient
		fields = ('firstname', 'lastname', 'profilePic', 'dateOfBirth', 'ssn', 'address', 'city', 'state', 'zip',
		          'gender', 'id', 'phone')

class InsuranceInfoForm(forms.ModelForm):
	class Meta:
		model = Insurance
		fields =('patient','doctor','companyName', 'contactNum','insID',
				 'insNetwork')

class MedicalChartForm(forms.ModelForm):
	class Meta:
		model = medicalChart
		fields=('date','patient','doctor','reason_for_visit','height','weight','blood_pressure','temperature','pulse','diagnosis','additionalNotes')

class GetUserID(forms.Form):
	patientID = forms.IntegerField(label="patientID")

class PrescriptionInfo(forms.ModelForm):
	class Meta:
		model = Prescription
		fields = ('date', 'patient','doctor','medication', 'quantity', 'length',
				  'dosage', 'refill_count')

class BillingForm(forms.ModelForm):
	class Meta:
		model = BillingLog
		fields = ('patient','doctor','date','procedure','amount')
