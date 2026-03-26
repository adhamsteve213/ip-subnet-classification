from django.urls import path

from .views import subnet_calculator

app_name = "subnetcalc"

urlpatterns = [
	path("", subnet_calculator, name="home"),
]

