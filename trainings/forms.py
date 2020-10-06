from django import forms
from .models import Training

# add a the datepicker https://www.youtube.com/watch?v=I2-JYxnSiB0
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput):
    input_type = 'date'

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training     
        fields = ['sport', 
                  'adress', 
                  'date',
                  'description']
        widgets = {
            'sport': forms.TextInput(attrs={"placeholder":"your sport"}),
            'adress': forms.TextInput(attrs={"placeholder":"City/Town, Street"}),
            'description': forms.TextInput(attrs={"placeholder":"City/Town, Street"}),
            'date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }