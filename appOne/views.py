from django.shortcuts import render
from .forms import LoginForm
from .forms import PostAppointment
from .forms import UserForm,PatientProfileInfoForm
from .forms import PostBill
from .models import Appointment
from .models import Patient
from .models import Doctor
from .models import medicalChart
from .models import Prescription
from .forms import GetUserID
from .forms import BillingForm
from .forms import PrescriptionInfo
from .models import BillingLog
from .models import Insurance
from .forms import InsuranceInfoForm
# Create your views here.
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import PostAppointment
from .forms import MedicalChartForm
from datetime import date
def index(request):
    return render(request,'appOne/index.html')


def login_view(request):
    if (request.user.is_authenticated()):
        return HttpResponseRedirect('/home')
        
        

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home')

                else:
                    print("Failure point1\n\n")
                    return render(request, 'appOne/index.html', {'form': form})
            else:
                print("Failure point2\n\n")
                return render(request, 'appOne/index.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'appOne/index.html', {'form' : form})


def logout_view(request):

    logout(request)
    return HttpResponseRedirect('/')

def post_appointment(request):

    if request.method == 'POST':
        form = PostAppointment(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            patientID = form.cleaned_data["patient"]
            doctorID = form.cleaned_data["doctor"]
            comments = form.cleaned_data["comments"]

            #Time to find patient object
            patient = Patient.objects.filter(id = patientID)[0]
            doctor = Doctor.objects.filter(id=doctorID)[0]

            newAppointment = Appointment(date=date, time=time, patient=patient,
                               doctor=doctor, comments=comments)
            newAppointment.save()
            return HttpResponseRedirect('/')

        else:
            HttpResponseRedirect('/')

    else:
        return render(request, 'appOne/makeAppointment.html', {'form': PostAppointment})

def post_bill(request):
    if request.method == 'POST':
        bill_form = PostBill(request.POST)

        if bill_form.is_valid():
            patientID = bill_form.cleaned_data["patient"]
            doctorID = bill_form.cleaned_data["doctor"]
            procedure = bill_form.cleaned_data["procedure"]
            date = bill_form.cleaned_data["date"]
            amount = bill_form.cleaned_data["amount"]
            patient = Patient.objects.filter(id=patientID)[0]
            doctor = Doctor.objects.filter(id=doctorID)[0]
            newBill = BillingLog(date=date, patient=patient, doctor=doctor, amount=amount, procedure=procedure)
            newBill.save()
            return render(request,'appOne/displayBillingLog.html')
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'appOne/addBill.html',{'bill_form':PostBill})

def add_insurance(request):
    if request.method == 'POST':
        ins_form = InsuranceInfoForm(request.POST)

        if ins_form.is_valid():
            patientID = ins_form.cleanedData["patient"]
            doctorID = ins_form.cleanedData["doctor"]
            companyName = ins_form.cleanedData['companyName']
            contactNum = ins_form.cleanedData['contactNum']
            insID = ins_form.cleanedData['insID']
            insNetwork = ins_form.cleanedData['insNetwork']
            patient = Patient.objects.filter(id=patientID)[0]
            doctor = Doctor.objects.filter(id=doctorID)[0]
            newInsurance = Insurance(patient=patient, doctor=doctor, companyName=companyName,
                                     contactNum=contactNum, insID=insID, insNetwork=insNetwork)
            newInsurance.save()
            return render(request,'appOne/displayInsurance.html')
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'appOne/addInsurance.html',{'ins_form':InsuranceInfoForm})


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = PatientProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profilePic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profilePic = request.FILES['profilePic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = PatientProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'appOne/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})




def displayMedicalCharts(request):

    form = GetUserID(request.POST)

    if request.method == 'POST' and form.is_valid() and request.user.is_staff == True:

        patientID = form.cleaned_data["patientID"]
        if request.user.is_staff:


            patient = Patient.objects.filter(id=patientID)
            medicalCharts = medicalChart.objects.filter(patient=patient)

            # appointments = Appointment.objects.all()
            mapping = {
                'medicalCharts': medicalCharts
            }
            return render(request, 'appOne/display_MedicalCharts.html', mapping)


        else:
            return HttpResponseRedirect('/')
    elif (request.user.is_authenticated() and (request.user.is_staff == False)):

            print("\n\nuser.id:")
            print(request.user.id)
            patientID = request.user.id
            patient = Patient.objects.filter(user_id=patientID)

            print("\n\npatient")
            print(patient)

            medicalCharts = medicalChart.objects.filter(patient=patient)

            mapping = {
                'medicalCharts': medicalCharts
            }

            return render(request, 'appOne/display_MedicalCharts.html', mapping)

    return render(request, 'appOne/display_MedicalCharts.html', {'form': GetUserID})


def displayAppointments(request):

    if (request.user.is_authenticated() and (request.user.is_staff == False)):
        current_user = request.user

        patient = Patient.objects.filter(user_id=current_user.id)
        appointments = Appointment.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by(
                'date')

        # appointments = Appointment.objects.all()
        mapping = {
            'appointments': appointments
        }

        return render(request, 'appOne/displayAppointments.html', mapping)

    elif (request.user.is_authenticated() and (request.user.is_staff == True)):
        appointments = Appointment.objects.all().filter(date__gte=(date.today())).order_by(
                'date')
        mapping = {
            'appointments': appointments
        }
        return render(request, 'appOne/displayAppointments.html', mapping)

    else:
        return HttpResponseRedirect('/')

def displayBillingLog(request):

    if request.user.is_authenticated() and (request.user.is_staff == False):
        current_user = request.user
        patient = Patient.objects.filter(user_id=current_user.id)
        billingLogs = BillingLog.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by(
            'date'
        )
        mapping = {
            'billingLogs': billingLogs
        }
        return render(request, 'appOne/displayBillingLog.html', mapping)
    elif request.user.is_authenticated() and (request.user.is_staff == True):
    	return render(request,'appOne/displayBillingLog.html')
    else:
        return HttpResponseRedirect('/')

def displayInsurance(request):
    if request.user.is_authenticated() and (request.user.is_staff == False):
        current_user = request.user
        patient = Patient.object.filter(user_id=current_user.id)
        insurances = Insurance.objects.filter(patient=patient).filter(date_gte=(date.today())).order_by(
            'date'
        )
        mapping = {
            'insurances': insurances
        }
        return render(request, 'appOne/displayInsurance.html', mapping)
    elif request.user.is_authenticated() and (request.user.is_staff == True):
        return render(request, 'appOne/displayInsurance.html')
    else:
        return HttpResponseRedirect('/')

def viewPatientBillView(request):
    bill_form = GetUserID(request.POST)
    if request.method == 'POST' and bill_form.is_valid() and request.user.is_staff == 'True':
        patientID = bill_form.cleaned_data["patientID"]
        patient = Patient.objects.filter(id=patientID)
        billingLogs = BillingLog.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by('date')
        mapping = {
            'billingLogs':billingLogs
        }
        return render(request,'appOne/displayBillingLog.html', mapping)
    else:
        patientID = bill_form.cleaned_data["patientID"]
        patient = Patient.objects.filter(id=patientID)
        billingLogs = BillingLog.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by('date')
        mapping = {
            'billingLogs': billingLogs
        }
        return render(request, 'appOne/displayBillingLog.html', mapping)

def medicalChartView(request):
    if request.method == 'POST':

        medical_chart_form = MedicalChartForm(request.POST)

        if medical_chart_form.is_valid():
            date = medical_chart_form.cleaned_data["date"]
            reason_for_visit= medical_chart_form.cleaned_data["reason_for_visit"]
            height = medical_chart_form.cleaned_data["height"]
            weight = medical_chart_form.cleaned_data["weight"]
            temperature = medical_chart_form.cleaned_data["temperature"]
            pulse = medical_chart_form.cleaned_data["pulse"]
            diagnosis = medical_chart_form.cleaned_data["diagnosis"]
            additionalNotes = medical_chart_form.cleaned_data["additionalNotes"]
            patientID = medical_chart_form.cleaned_data["patient"]
            doctorID = medical_chart_form.cleaned_data["doctor"]
            blood_pressure = medical_chart_form.cleaned_data["blood_pressure"]



            newChart = medicalChart(date=date,patient=patientID, doctor=doctorID,reason_for_visit=reason_for_visit,
                                    height=height,weight=weight,temperature=temperature,
                                    pulse=pulse,blood_pressure=blood_pressure,
                                    diagnosis=diagnosis,additionalNotes=additionalNotes)
            newChart.save()
            return HttpResponseRedirect('/')

        else:
            HttpResponseRedirect('/')

    else:
        return render(request, 'appOne/medicalChart.html', {'medical_chart_form':MedicalChartForm})



def patientHomeView(request):

    form = GetUserID(request.POST)

    if request.method == 'POST' and form.is_valid() and request.user.is_staff == True:

        patientID = form.cleaned_data["patientID"]
        if request.user.is_staff:

            patient = Patient.objects.filter(id=patientID)
            #medicalCharts = medicalChart.objects.filter(patient=patient)
            # find appointments for patient that are greater than today, order by date and limit results to 3
            appointments = Appointment.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by(
                'date')[:3]
            prescriptions = Prescription.objects.filter(patient=patient).filter(date__gte=(date.today())).order_by(
                'date')[:3]
            billingLogs = BillingLog.objects.filter(patient=patient)
            # appointments = Appointment.objects.all()
            mapping = {
                'patient': patient,
                'appointments': appointments,
                'prescriptions': prescriptions,
                'billingLogs':billingLogs
            }

            return render(request, 'appOne/patientHome.html', mapping)


        else:
            return HttpResponseRedirect('/')
    elif (request.user.is_authenticated() and (request.user.is_staff == False)):

        print("\n\nuser.id:")
        print(request.user.id)
        patientID = request.user.id
        patient = Patient.objects.filter(user_id=patientID)
        # find appointments for patient that are greater than today, order by date and limit results to 3
        appointments = Appointment.objects.filter(patient = patient).filter(date__gte = (date.today())).order_by('date')[:3]
        prescriptions = Prescription.objects.filter(patient = patient).filter(date__gte = (date.today())).order_by('date')[:3]
        billingLogs = BillingLog.objects.filter(patient=patient)
        print("\n\npatient")
        print(patient)

        #medicalCharts = medicalChart.objects.filter(patient=patient)

        mapping = {
            'patient': patient,
            'appointments' : appointments,
            'prescriptions' : prescriptions,
            'billingLogs':billingLogs
        }

        return render(request, 'appOne/patientHome.html', mapping)

    return render(request, 'appOne/patientHome.html', {'form': GetUserID})


def post_prescription(request):

    if request.method == 'POST':

        prescription_form = PrescriptionInfo(request.POST)

        if prescription_form.is_valid():
            date = prescription_form.cleaned_data["date"]
            patientID = prescription_form.cleaned_data["patient"]
            doctorID = prescription_form.cleaned_data["doctor"]
            medication = prescription_form.cleaned_data["medication"]
            quantity = prescription_form.cleaned_data["quantity"]
            length = prescription_form.cleaned_data["length"]
            dosage = prescription_form.cleaned_data["dosage"]
            refill_count = prescription_form.cleaned_data["refill_count"]

            newPrescription = Prescription(date=date, patient=patientID, doctor=doctorID, medication=medication,
                                               quantity=quantity, length=length, dosage=dosage,
                                               refill_count=refill_count)
            newPrescription.save()
            return HttpResponseRedirect('/')

        else:
            HttpResponseRedirect('/')

    else:
        return render(request, 'appOne/addPrescription.html', {'prescription_form': PrescriptionInfo})


def viewProfileInfoView(request):

    if request.method == 'GET' and request.user.is_staff == False:

        patient = Patient.objects.filter(user_id=request.user.id)
        insurance = Insurance.objects.filter(patient=patient)
        print(patient)
        print(request.user.id)
        print(insurance)
        # appointments = Appointment.objects.all()
        mapping = {
            'patient': patient,
            'insurance':insurance
         }
        print("hello\n\n\n")

        return render(request, 'appOne/viewProfile.html', mapping)
    else:
        print("hello\n\n\n")
        HttpResponseRedirect('/')