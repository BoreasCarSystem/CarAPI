from django import forms

class SetTemperatureForm(forms.Form):
    temperature = forms.CharField(label="temperature", max_length="50")
