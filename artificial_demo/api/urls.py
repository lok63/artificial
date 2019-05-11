from django.contrib import admin
from django.urls import path,include
from .views import store_dataset, Store_Data

urlpatterns = [
    path('upload_data/', Store_Data.as_view()),
]