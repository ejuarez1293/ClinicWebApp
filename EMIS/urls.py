"""EMIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from appOne import views
from EMIS import settings
from django.views.static import serve



urlpatterns = [
    url(r'^$',views.login_view,name='index'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^appOne/',include('appOne.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^appointment/$', views.post_appointment, name='post_appointment'),
    url(r'^viewAppointments/$', views.displayAppointments, name='view_appointments'),
    url(r'^medicalchart/$', views.displayMedicalCharts, name='view_medicalcharts'),
    url(r'^newmedicalchart/$',views.medicalChartView,name='medical_chart'),
    url(r'^home/$',views.patientHomeView,name='patientHomeView'),
    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
    url(r'^BillingLog/$', views.displayBillingLog, name='BillingLog'),
    url(r'^postBill/$', views.post_bill, name="post_bill"),
    url(r'^LookUpBill/$',views.viewPatientBillView, name='viewPatientBillView'),
    url(r'^addPrescription',views.post_prescription, name='post_prescription'),
    url(r'^viewProfile/$',views.viewProfileInfoView, name='viewProfile'),
    url(r'^addInsurance/$',views.add_insurance, name = 'add_insurance'),
    url(r'^viewInsurance/$',views.displayInsurance,  name = 'displayInsurance')

]
