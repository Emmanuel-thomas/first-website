from django import forms
from django.forms.widgets import Widget

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
     
)
RESULT_CHOICES = (
    ('#1', 'transaction'),
    ('#2', 'sales date'),     
)

class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)
    # num = forms.IntegerField(widget=forms.NumberInput())
    

    # def clean(self) -> Dict[str, Any]:
    #     cleaned_data= super().clean()