# urls.py

from django.urls import path
from django.views.generic import RedirectView  # It provides a convenient way to perform URL redirections
from django.conf import settings
from . import views
from .views import index, contact, contact_form
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('index.html', contact_form, name='contact_form'),
    path('login.html', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register.html', views.register, name='register'),
    path('edit_profile.html', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('charts.html', views.charts, name='charts'),
    path('robot.html', views.robot, name='robot'),
    path('doctors.html', views.doctors, name='doctors'),
    path('courses.html', views.courses, name='courses'),
    path('donation.html', views.donation, name='donation'),
    path('test.html', views.test, name='test'),
    path('test_result.html', views.test_result, name='test_result'),
    path('detection.html', views.detection, name='detection'),
    path('detection_result.html', views.detection_result, name='detection_result'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)