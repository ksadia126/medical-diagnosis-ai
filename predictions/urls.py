"""
URL configuration for predictions app.
"""
from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.home, name='home'),
    path('heart-disease/', views.heart_disease_prediction, name='heart_disease'),
    path('lung-cancer/', views.lung_cancer_prediction, name='lung_cancer'),
    path('diabetes/', views.diabetes_prediction, name='diabetes'),
    path('parkinsons/', views.parkinsons_prediction, name='parkinsons'),
    path('thyroid/', views.thyroid_prediction, name='thyroid'),
]