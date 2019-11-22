from django import forms

class LinkForm(forms.Form):
    link = forms.URLField(label='Link', max_length=1000)