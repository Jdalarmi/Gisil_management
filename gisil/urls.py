from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gisil_values/', views.entry_value, name="gisil-values"),
    path('customer/', views.customer, name="gisil-customer"),
]
