from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gisil_values/', views.entry_value, name="gisil-values"),
    path('customer/', views.customer, name="gisil-customer"),
    path('all_zero/', views.reset_all_zero, name='all-zero'),
    path('edit_values/', views.edit_values, name='edit-values'),
]
