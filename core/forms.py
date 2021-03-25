from django import forms
from django.forms import widgets
from core.models import Questions

class GetAnswer(forms.Form):
    answer1 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer2 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer3 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer4 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer5 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer6 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer7 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer8 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer9 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))
    answer10 = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
        'cols':118,
        'placeholder': 'Enter your detailed answer here....',
    }))