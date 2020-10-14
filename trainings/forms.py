from django import forms
from .models import Training

class TrainingFilterForm(forms.Form):
    timeChoices = [("week","this week"), ("month", "this month"), ("noLimit","all upcoming")]
    timePeriod = forms.CharField(
                    widget=forms.Select(  
                    choices=timeChoices,
                    ))
    sportFilter = forms.CharField(label='sport',
                                    required=False,
                                    widget=forms.TextInput(
                                    attrs={"placeholder":"sport",
                                            }))


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
                  'maxParticipants',
                  'description']
        widgets = {
            'sport': forms.TextInput(attrs={"placeholder":"your sport"}),
            'adress': forms.TextInput(attrs={"placeholder":"City/Town, Street"}),
            'description': forms.Textarea(
                                attrs={
                                    "placeholder":"Tell others what to expect!",
                                    "cols":90,
                                    "rows":10}),
            'date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }