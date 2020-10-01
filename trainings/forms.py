from django import forms
from .models import Training

# add a the datepicker https://www.youtube.com/watch?v=I2-JYxnSiB0
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput):
    input_type = 'date'

class TrainingForm(forms.ModelForm):
    time = forms.DateField(widget=DateInput)
    sport = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder":"your sport"}))
    adress = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder":"City/Town, Street"}))
    class Meta:
          model = Training     
          fields = ['sport', 
                    'adress', 
                    'time']