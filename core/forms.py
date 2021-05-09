from django import forms

class GetAnswer(forms.Form):
    file = forms.FileField()