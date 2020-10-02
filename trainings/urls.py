from django.urls import path
from django.views.i18n import JavaScriptCatalog


from . import views

app_name = "trainings"

urlpatterns = [
    path("", views.index, name="index"),
    path("jsi18n", JavaScriptCatalog.as_view(), name='js-catalog')
]