from django import forms
from .models import Training


class TrainingFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TrainingFilterForm, self).__init__(*args, **kwargs)
        self.fields['timePeriod'].label = "time period"
    timeChoices = [("week","this week"), ("month", "this month"), ("noLimit","all upcoming")]
    timePeriod = forms.CharField(
                    widget=forms.Select(  
                    choices=timeChoices,
                    ))
    sportFilter = forms.CharField(label='sport',
                                    required=False,
                                    widget=forms.TextInput(
                                    attrs={"placeholder":"e.g. hiking",}
                                    ))


# add a the datepicker https://www.youtube.com/watch?v=I2-JYxnSiB0
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput):
    input_type = 'date'

class TrainingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['sport'].label = "Activity"
        self.fields['adress'].label = "Where to meet?"        
        self.fields['maxParticipants'].label = "Maximum participants"
        self.fields['date'].label = "When?"
        self.fields['description'].label = "Short description"

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
            'maxParticipants': forms.TextInput(attrs={
                                        # 'label': 'total participants',
                                        "placeholder":"maximum number of participants"}),
            'description': forms.Textarea(
                                attrs={
                                    "placeholder":"Tell others what to expect!",
                                    "cols":90,
                                    "rows":10}),
            'date': forms.DateTimeInput(attrs={'type':'datetime-local'})}
            # 'date': DateTimePickerInput(format="%Y-%m-%d %H:%M")}