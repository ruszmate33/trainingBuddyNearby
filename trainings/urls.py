from django.urls import path

from . import views

app_name = "trainings"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("<int:training_id>", views.training, name="training"),
    path("myTrainings", views.myTrainings, name="myTrainings"),
    path("<int:training_id>/toggleJoined", views.toggleJoined, name="toggleJoined"),
    path("<int:training_id>/deleteTraining", views.deleteTraining, name="deleteTraining"),
]