from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('services', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/new/', views.service_new, name='service_new'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
]