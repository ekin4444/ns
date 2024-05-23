# urls.py

from django.urls import path

from . import views
from .views import index, contact, contact_form

urlpatterns = [
    path('', index, name='index'),
    path('index.html', contact_form, name='contact_form'),
    path('login.html', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register.html', views.register, name='register'),
    path('edit_profile.html', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('statistics.html', views.statistics, name='statistics'),
    path('robot.html', views.robot, name='robot'),
    path('doctors.html', views.doctors, name='doctors'),
    path('training.html', views.training, name='training')
]
