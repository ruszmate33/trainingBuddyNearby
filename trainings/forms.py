from django import forms
from .models import Training
# from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.admin import widgets                                       


# add a the datepicker https://www.youtube.com/watch?v=I2-JYxnSiB0
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput):
    input_type = 'date'

# try to separate date and time into two fields, maybe unify them in the model
class TrainingForm(forms.ModelForm):
    sport = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder":"your sport"}))
    adress = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder":"City/Town, Street"}))
    class Meta:
          model = Training     
          fields = ['sport', 
                    'adress',
                    'date',
                    'time', 
                    'dateTime']

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        self.fields['time'].widget = widgets.AdminTimeWidget()
        self.fields['dateTime'].widget = widgets.AdminSplitDateTime()