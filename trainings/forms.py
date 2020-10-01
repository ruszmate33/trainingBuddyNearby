from django import forms
from .models import Training

# add a the datepicker https://www.youtube.com/watch?v=I2-JYxnSiB0
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput):
    input_type = 'date'

class ExampleForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput)

class ExampleForm2(forms.Form):
    my_date_field = forms.DateTimeField(widget=DateTimeInput)


class TrainingForm(forms.ModelForm):
    time = forms.DateField(widget=DateInput)
    class Meta:
          model = Training     
          widgets = {'time': DateInput()}
          fields = ('sport', 'adress', 'time')