from django.contrib import admin
from django.urls import path,include
from .views import upload_file,reset_BankModel,list_dataset, train_evaluate

urlpatterns = [
    path('machine-learning/', upload_file),
    path('machine-learning/reset', reset_BankModel, name="reset"),
    path('machine-learning/train_evaluate', train_evaluate, name="train_evaluate"),
    path('list_dataset/', list_dataset),
]