from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class GenerateOrderForm(forms.Form):
    number = forms.IntegerField(label = '', widget=forms.NumberInput(attrs={'placeholder':'Введите количество сгенерированых заказов'}))

    def clean_number(self):
        number = self.cleaned_data['number']
        if int(number) <= 0:
            raise forms.ValidationError('Введите число больше 0.')
        return number