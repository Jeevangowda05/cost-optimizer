from django.urls import path

from . import views

app_name = 'ml'

urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('datasets/upload/', views.upload_dataset_view, name='upload_dataset'),
]
