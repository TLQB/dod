from django import forms
from django.core.validators import FileExtensionValidator

class DataProcessingForm(forms.Form):
    input_filename = forms.FileField(label='Input Filename', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])
    output_filename = forms.CharField(label='Output Filename', required=True, initial='output_excel.xlsx')
    sheet_name = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)
    brand = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)
    column = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sheet_name'].choices = []
        self.fields['brand'].choices = []
        self.fields['column'].choices = []