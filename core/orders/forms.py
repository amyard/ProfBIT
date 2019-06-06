from django import forms
from datetime import date, datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class GenerateOrderForm(forms.Form):
    number = forms.IntegerField(label = '', widget=forms.NumberInput(attrs={'placeholder':'Введите количество сгенерированых заказов'}))

    def clean_number(self):
        number = self.cleaned_data['number']
        if int(number) <= 0:
            raise forms.ValidationError('Введите число больше 0.')
        return number


class OrderByDateForm(forms.Form):
    start_period = forms.DateField(label='Начальная дата',initial=datetime(2018,1,1), widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    end_date = forms.DateField(label='Конечная дата', initial=datetime.now(), widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))

    def clean(self):
        start_period = self.cleaned_data['start_period']
        end_date = self.cleaned_data['end_date']

        if start_period > date.today() or end_date > date.today():
            raise forms.ValidationError('Вы не можете использовать дату больше Сегодняшней даты.')

        if start_period == end_date:
            raise forms.ValidationError('Для корректого отобржения статистики конечная дата должна быть больше хотя бы на один день, чем начальная дата.')

        if start_period > end_date:
            raise forms.ValidationError('Начальная дата не может быть больше Конечной даты.')

        if start_period < date(2018,1,1):
            raise forms.ValidationError('Вы не можете использовать дату меньше 2018-01-01.')