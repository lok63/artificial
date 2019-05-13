from django.contrib import admin
from django.urls import path,include
from .views import upload_file,reset_BankModel,list_dataset, train_evaluate,prediction_new,prediction_list

urlpatterns = [
    path('machine-learning/', upload_file, name="machine-learning" ),
    path('machine-learning/reset', reset_BankModel, name="reset"),
    path('machine-learning/train_evaluate', train_evaluate, name="train_evaluate"),
    path('machine-learning/predictions', prediction_list, name="predictions" ),
    path('machine-learning/predictions/new', prediction_new, name="prediction_new" ),
    path('list_dataset/', list_dataset),
]