from django.conf.urls import url
from appOne import views

# SET THE NAMESPACE!
app_name = 'appOne'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
]
