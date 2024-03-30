from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="dashboard"),
    path('add-dashboard', views.add_dashboard, name="add-dashboard")
]
