from django.urls import path
from . import views

app_name = "prediction"

urlpatterns = [
    path("", views.home, name="home"),
    path("prediction/", views.predict, name="predict"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
