from django.urls import path, include
from django.conf.urls import url
from . import views
from .models import Clients
from med.views import MedAutocomplete, ServiceAutocomplete

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('', views.med_list, name='med_list'),
    path('report', views.med_report, name='med_report'),
    path('med/new/', views.med_new, name='med_new'),
    path('med/<int:pk>/edit/', views.med_edit, name='med_edit'),
    path('med/<int:pk>/delete/', views.med_delete, name='med_delete'),
    url(r'^med-autocomplete/$', MedAutocomplete.as_view(), name='med-autocomplete'),
    url(r'^service-autocomplete/$', ServiceAutocomplete.as_view(), name='service-autocomplete'),
]