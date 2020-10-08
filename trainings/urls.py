from django.urls import path

from . import views

app_name = "trainings"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("<int:training_id>", views.training, name="training"),
    path("<int:training_id>/join", views.join, name="join"),
    path("<int:training_id>/signout", views.signout, name="signout"),
]