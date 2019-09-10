from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('clients', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/new/', views.client_new, name='client_new'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
]