from django.forms.widgets import TextInput
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput



class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'


class TrainingFilter(django_filters.FilterSet):   
    sport = CharFilter(field_name = "sport", lookup_expr = 'icontains')
    date = DateFilter(field_name = "date", lookup_expr='lte')
    class Meta:
        model = Training
        fields = ['sport', 'date']
        widgets = {
            'sport':TextInput(
                attrs= {
                    "placeholder":"sport"
                }),
            'date': DateTimePickerInput(
                attrs= {
                    "placeholder":"%Y-%m-%d %H:%M"})}